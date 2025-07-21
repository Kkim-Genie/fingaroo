#!/usr/bin/env python3

import sys
import os

# Add the app directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from app.agent.tools.search.search_knowledge_base import search_knowledge_base

def main():
    query = "트럼프의 관세정책"
    print(f"검색 쿼리: {query}")
    print("-" * 50)
    
    try:
        result = search_knowledge_base(query)
        print("검색 결과:")
        print(result)
    except Exception as e:
        print(f"오류 발생: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 