# 2. agent.py

from typing import List, Tuple, Dict, Any, TypedDict, Annotated
from langgraph.graph import StateGraph, END
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain_ollama import ChatOllama
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.tools import Tool
from langchain.agents import AgentExecutor
from langchain.agents.react.agent import create_react_agent
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
import sqlite3

class SQLiteTools:
    def __init__(self, db_path: str):
        self.db_path = db_path
        
    def execute_query(self, query: str) -> List[Tuple]:
        """
        Function to execute SQL queries
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(query)
                return cursor.fetchall()
        except Exception as e:
            return f"Error execute_query occurred: {str(e)}"
            
    def get_table_schema(self, *args) -> Dict[str, List[str]]:  
        """Get schema information for all tables"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()

                cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
                tables = cursor.fetchall()
                
                schema = {}
                for table in tables:
                    table_name = table[0]

                    cursor.execute(f"PRAGMA table_info({table_name})")
                    columns = cursor.fetchall()

                    schema[table_name] = [
                        {
                            "name": col[1],
                            "type": col[2],
                            "notnull": col[3],
                            "pk": col[5]
                        } for col in columns
                    ]
                return schema
        except Exception as e:
            return f"Error get_table_schema occurred: {str(e)}"

class AgentState(TypedDict):
    input: str
    output: Any
    messages: List[Any]

class SQLiteAgent:
    def __init__(self, db_path: str, model_name: str = "deepseek-r1:8b"):
        self.db_tools = SQLiteTools(db_path)
        
        self.llm = ChatOllama(
            model=model_name,
            temperature=0,  # ความแปรปรวนในการสร้างข้อความ ใช้ 0 สำหรับความแม่นยำสูงสุด
            callbacks=[StreamingStdOutCallbackHandler()],
            base_url="http://localhost:11434",
            streaming=True
        )
        
        self.tools = [
            Tool(
              name="execute_query",
              func=self.db_tools.execute_query,
              description="Execute a SQL query. Input should be a valid SQL query string."
            ),
            Tool(
                name="get_schema",
                func=self.db_tools.get_table_schema,
                description="Get the database schema. No input needed."
            )
        ]
        
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a SQL database assistant. Follow the format below EXACTLY, including EXACT spacing and punctuation:

            Thought: [your reasoning]
            Action: [tool name]
            Action Input: [tool input]
            Observation: [tool output]
            ... (this Thought/Action/Action Input/Observation can repeat if needed)
            Thought: [your conclusion]
            Final Answer: [your response]

            Available tools:
            {tool_names}

            {tools}

            Remember:
            1. ALWAYS start with "Thought:"
            2. ALWAYS include "Action:" after "Thought:"
            3. ALWAYS follow the exact format above
            4. NEVER include multiple actions without observations between them
            5. NEVER skip steps in the format"""),
                    ("human", "{input}"),
                    ("ai", "{agent_scratchpad}")
        ])
          
        self.agent = create_react_agent(
            llm=self.llm,
            tools=self.tools,
            prompt=self.prompt
        )
        
        self.agent_executor = AgentExecutor(
            agent=self.agent,
            tools=self.tools,
            verbose=True,
            return_intermediate_steps=True,  # สำหรับการแสดงข้อความระหว่างการทำงาน
            handle_parsing_errors=True,  # จัดการข้อผิดพลาดในการแปลงข้อความ
            max_iterations=5  # จำกัดจำนวนรอบการทำงาน (เพื่อป้องกันการวนลูป)
        )

    def run(self, query: str) -> Any:
        """
        Run Agent to process queries
        """
        try:
          def process_agent(state: Dict) -> Dict:
              # Call agent executor
              result = self.agent_executor.invoke({
                  "input": state["input"],
                  "agent_scratchpad": state.get("messages", [])
              })
              
              # Create messages
              messages = []
              if "intermediate_steps" in result:
                  for step in result["intermediate_steps"]:
                      action, output = step
                      messages.extend([
                          AIMessage(content=str(action)),
                          HumanMessage(content=str(output))
                      ])
              
              # Update state
              return {
                  "input": state["input"],
                  "output": result.get("output", ""),
                  "messages": messages
              }
          
          workflow = StateGraph(state_schema=AgentState)
          
          workflow.add_node("agent", process_agent)
          
          workflow.set_entry_point("agent")
          
          workflow.add_edge("agent", END)
          
          app = workflow.compile()
          
          # Create initial state
          initial_state = {
              "input": query,
              "output": None,
              "messages": []
          }
          
          # Run workflow
          result = app.invoke(initial_state)
          
          # Get results
          return result["output"]
        except ValueError as e:
            if "Could not parse LLM output" in str(e):
                return f"Error: The model response could not be parsed. Original query: {query}"
            raise
        except Exception as e:
            return f"An error occurred: {str(e)}"

# Usage example
# Command line interface
if __name__ == "__main__":
    import argparse
    import sys
    
    # สร้าง argument parser
    parser = argparse.ArgumentParser(description='SQLite AI Assistant')
    parser.add_argument('--db', type=str, default="products.db", help='Database file path')
    parser.add_argument('--model', type=str, default="deepseek-r1:8b", help='Ollama model name')
    parser.add_argument('prompt', type=str, nargs='+', help='Natural language prompt')
    
    # Parse arguments
    args = parser.parse_args()
    
    # สร้าง Agent
    agent = SQLiteAgent(args.db, model_name=args.model)
    
    try:
        # รวมคำสั่งเป็น string เดียว
        prompt = ' '.join(args.prompt)
        
        # ส่งคำสั่งไปให้ agent
        result = agent.run(prompt)
        print(result)
            
    except Exception as e:
        print(f"เกิดข้อผิดพลาด: {str(e)}")