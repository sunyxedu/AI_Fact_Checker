from statement_extractor import Statement
from article_finder import find_articles, Article
from dataclasses import dataclass
from typing import List
import wikipedia
import json

"""
We take a list of Statements from the YouTube video and compute
truthiness scores for all of them using a mixture of methods.

For simple cases, we can rely on an LLM to determine truthiness. If it
determines that the issue is controversial or confusing we can
fall back to search results and Google Fact Check API.

Outputs should be normalised floats between 0 and 1.
"""
def fact_check(statements: List[Statement]) -> List[float]:
    from openai import OpenAI
    client = OpenAI()
    
    def check_trivial(statement: str) -> tuple[bool, float]:
        """Returns (is_trivial, truthiness)"""
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are an expert at determining if statements are trivially true/false or require deeper fact checking."},
                {"role": "user", "content": f"Is this statement trivially true/false or does it require deeper fact checking? If trivial, what is the truthiness (0-1)?\n\nStatement: {statement}"}
            ],
            functions=[{
                "name": "analyze_statement",
                "description": "Analyzes if a statement is trivial and its truthiness",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "is_trivial": {
                            "type": "boolean",
                            "description": "Whether the statement can be trivially evaluated"
                        },
                        "truthiness": {
                            "type": "number",
                            "description": "If trivial, truthiness between 0-1",
                            "minimum": 0,
                            "maximum": 1
                        }
                    },
                    "required": ["is_trivial", "truthiness"]
                }
            }],
            function_call={"name": "analyze_statement"}
        )
        result = json.loads(response.choices[0].message.function_call.arguments)
        return result["is_trivial"], result["truthiness"]

    def check_historical(statement: str) -> bool:
        """Returns whether statement is about historical events"""
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Determine if a statement is about historical events or major past occurrences."},
                {"role": "user", "content": f"Is this statement about historical events or major past occurrences?\n\nStatement: {statement}"}
            ],
            functions=[{
                "name": "check_historical",
                "description": "Checks if statement is historical",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "is_historical": {
                            "type": "boolean",
                            "description": "Whether the statement is about historical events"
                        }
                    },
                    "required": ["is_historical"]
                }
            }],
            function_call={"name": "check_historical"}
        )
        result = json.loads(response.choices[0].message.function_call.arguments)
        return result["is_historical"]

    truth_scores = []
    for statement in statements:
        is_trivial, trivial_score = check_trivial(statement.text)
        
        if is_trivial:
            truth_scores.append(trivial_score)
            continue
            
        if check_historical(statement.text):
            # Try to find relevant Wikipedia articles
            try:
                # Search Wikipedia for relevant pages
                search_results = wikipedia.search(statement.text)
                if not search_results:
                    # If no Wikipedia results, treat as non-historical and use regular fact checking
                    articles = find_articles(statement.text)
                    articles_content = "\n\n".join([f"Title: {article.title}\nContent: {article.text}" for article in articles])
                else:
                    # Get full content of first few relevant Wikipedia pages
                    wiki_content = []
                    for title in search_results[:3]:
                        try:
                            page = wikipedia.page(title)
                            wiki_content.append(f"Title: {page.title}\nContent: {page.content}")
                        except wikipedia.exceptions.DisambiguationError as e:
                            # Handle disambiguation by getting first suggested page
                            try:
                                page = wikipedia.page(e.options[0])
                                wiki_content.append(f"Title: {page.title}\nContent: {page.content}")
                            except:
                                continue
                        except:
                            continue
                    
                    articles_content = "\n\n".join(wiki_content)
                
                # Use LLM to verify statement against Wikipedia content
                response = client.chat.completions.create(
                    model="gpt-4",
                    messages=[
                        {"role": "system", "content": "You are an expert historian tasked with verifying historical claims against Wikipedia sources. If the claim seems vague or cannot be definitively verified with the provided sources, indicate this in your assessment."},
                        {"role": "user", "content": f"Verify this historical claim against the following Wikipedia content. Claim: {statement.text}\n\nWikipedia content: {articles_content}"}
                    ],
                    functions=[{
                        "name": "verify_historical_claim",
                        "description": "Verifies a historical claim against Wikipedia sources",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "truthiness": {
                                    "type": "number",
                                    "description": "Truth score between 0 and 1",
                                    "minimum": 0,
                                    "maximum": 1
                                },
                                "is_vague": {
                                    "type": "boolean",
                                    "description": "Whether the claim is too vague to verify definitively"
                                }
                            },
                            "required": ["truthiness", "is_vague"]
                        }
                    }],
                    function_call={"name": "verify_historical_claim"}
                )
                result = json.loads(response.choices[0].message.function_call.arguments)
                
                if result["is_vague"]:
                    # For vague claims, fall back to Google fact check
                    articles = find_articles(statement.text)
                    articles_content = "\n\n".join([f"Title: {article.title}\nContent: {article.text}" for article in articles])
                    
                    response = client.chat.completions.create(
                        model="gpt-4",
                        messages=[
                            {"role": "system", "content": "You are an expert at fact checking claims against source material."},
                            {"role": "user", "content": f"Verify this claim against the following articles. Claim: {statement.text}\n\nArticles content: {articles_content}"}
                        ],
                        functions=[{
                            "name": "verify_claim",
                            "description": "Verifies a claim against sources",
                            "parameters": {
                                "type": "object",
                                "properties": {
                                    "truthiness": {
                                        "type": "number",
                                        "description": "Truth score between 0 and 1",
                                        "minimum": 0,
                                        "maximum": 1
                                    }
                                },
                                "required": ["truthiness"]
                            }
                        }],
                        function_call={"name": "verify_claim"}
                    )
                    result = json.loads(response.choices[0].message.function_call.arguments)
                
                truth_scores.append(result["truthiness"])
                
            except Exception as e:
                # On any error, fall back to regular fact checking
                articles = find_articles(statement.text)
                articles_content = "\n\n".join([f"Title: {article.title}\nContent: {article.text}" for article in articles])
                
                response = client.chat.completions.create(
                    model="gpt-4",
                    messages=[
                        {"role": "system", "content": "You are an expert at fact checking claims against source material."},
                        {"role": "user", "content": f"Verify this claim against the following articles. Claim: {statement.text}\n\nArticles content: {articles_content}"}
                    ],
                    functions=[{
                        "name": "verify_claim",
                        "description": "Verifies a claim against sources",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "truthiness": {
                                    "type": "number",
                                    "description": "Truth score between 0 and 1",
                                    "minimum": 0,
                                    "maximum": 1
                                }
                            },
                            "required": ["truthiness"]
                        }
                    }],
                    function_call={"name": "verify_claim"}
                )
                result = json.loads(response.choices[0].message.function_call.arguments)
                truth_scores.append(result["truthiness"])
        else:
            articles = find_articles(statement.text)
            articles_content = "\n\n".join([f"Title: {article.title}\nContent: {article.text}" for article in articles])
            
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are an expert at fact checking claims against source material."},
                    {"role": "user", "content": f"Verify this claim against the following articles. Claim: {statement.text}\n\nArticles content: {articles_content}"}
                ],
                functions=[{
                    "name": "verify_claim",
                    "description": "Verifies a claim against sources",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "truthiness": {
                                "type": "number",
                                "description": "Truth score between 0 and 1",
                                "minimum": 0,
                                "maximum": 1
                            }
                        },
                        "required": ["truthiness"]
                    }
                }],
                function_call={"name": "verify_claim"}
            )
            result = json.loads(response.choices[0].message.function_call.arguments)
            truth_scores.append(result["truthiness"])
            
    return truth_scores