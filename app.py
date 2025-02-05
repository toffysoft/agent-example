# app.py
import streamlit as st
import json
from agent import SQLiteAgent

def main():
    st.set_page_config(
        page_title="SQLite AI Assistant",
        page_icon="🤖",
        layout="wide"
    )

    st.title("🤖 SQLite AI Assistant")

    # Sidebar configuration
    with st.sidebar:
        st.header("⚙️ Configuration")
        model_name = st.selectbox(
            "Select Model",
            ["deepseek-r1:8b"],
            index=0
        )
        
        db_path = st.text_input(
            "Database Path",
            value="products.db"
        )
        
        st.markdown("---")
        st.markdown("""
        ### Example Queries:
        - show database schema
        - show first 5 rows from products table
        - count total records in products table
        """)

    # Main content
    query = st.text_area("Enter your query:", height=100)
    
    if st.button("🚀 Execute Query", type="primary"):
        if query:
            try:
                with st.spinner("Processing..."):
                    # Create agent and process query
                    agent = SQLiteAgent(db_path, model_name=model_name)
                    result = agent.run(query)
                    
                    # Show results
                    st.success("Query executed successfully!")
                    
                    # Add to history
                    if 'history' not in st.session_state:
                        st.session_state.history = []
                    st.session_state.history.append((query, result))
                    
                    # Check if result is JSON
                    try:
                        if isinstance(result, str):
                            json_result = json.loads(result)
                            st.json(json_result)
                        else:
                            st.write(result)
                    except:
                        st.write(result)
                    
            except Exception as e:
                st.error(f"Error: {str(e)}")
        else:
            st.warning("Please enter a query")

    # History section
    with st.expander("📜 Query History", expanded=False):
        if 'history' not in st.session_state:
            st.session_state.history = []
            
        # Show query history
        for idx, (past_query, past_result) in enumerate(st.session_state.history):
            st.markdown(f"**Query {idx+1}:** {past_query}")
            st.markdown(f"**Result:** {past_result}")
            st.markdown("---")

if __name__ == "__main__":
    main()