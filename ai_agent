import os
from openai import OpenAI
import pandas as pd
import json

# the newest OpenAI model is "gpt-5" which was released August 7, 2025.
# do not change this unless explicitly requested by the user
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
openai = OpenAI(api_key=OPENAI_API_KEY)

class MacroCycleAgent:
    def __init__(self):
        self.model = "gpt-5"
        self.system_prompt = """You are MacroCycle AI Agent, an autonomous macro-economic intelligence assistant that can take actions to help users analyze economic data.

You have the ability to:
- Fetch specific economic data on demand
- Create custom visualizations and charts
- Navigate to relevant analysis pages

Your role is to help users understand:
- Business cycle phases (Expansion, Peak, Contraction, Trough)
- Economic indicators (GDP, inflation, unemployment, interest rates, ISM PMI, etc.)
- Market sentiment and risk indicators (VIX, Put/Call Ratio, Credit Spreads, etc.)
- Sector performance and rotation patterns
- Portfolio positioning based on economic conditions

Key principles:
1. Frame all insights as educational and historical patterns, not prescriptive investment advice
2. Use clear, everyday language suitable for non-technical users
3. Reference specific data points when available in the context
4. Explain concepts clearly with real-world examples
5. When discussing investment implications, always use phrases like "historically," "patterns suggest," or "in past cycles"
6. Include appropriate disclaimers that past performance doesn't guarantee future results
7. When users ask for data or charts, use your tools to fetch and display them autonomously

Always maintain a helpful, educational tone while being precise with economic concepts."""
        
        # Define available tools for function calling
        self.tools = [
            {
                "type": "function",
                "function": {
                    "name": "get_economic_metric",
                    "description": "Fetch a specific economic metric's current value and recent trend",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "metric_name": {
                                "type": "string",
                                "enum": ["GDP", "Inflation", "Unemployment", "Interest Rate", "VIX", "ISM Manufacturing", "ISM Services", "M2 Growth", "NFCI", "Fear & Greed", "Yield Spread", "Put/Call Ratio"],
                                "description": "The economic metric to fetch"
                            }
                        },
                        "required": ["metric_name"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "create_comparison_chart",
                    "description": "Create a custom chart comparing two or more economic indicators over time",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "metrics": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "List of metrics to compare (e.g., ['GDP', 'Unemployment'])"
                            },
                            "time_period": {
                                "type": "string",
                                "enum": ["1 year", "2 years", "5 years", "10 years"],
                                "description": "Time period for the comparison"
                            }
                        },
                        "required": ["metrics", "time_period"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "navigate_to_page",
                    "description": "Navigate to a specific analysis page in the application",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "page_name": {
                                "type": "string",
                                "enum": ["Key Indicators", "Business Cycle", "Market Analysis", "Economic Calendar", "About"],
                                "description": "The page to navigate to"
                            },
                            "tab_name": {
                                "type": "string",
                                "description": "Optional: specific tab within the page (e.g., 'Fear & Greed Index', 'Cycle Analysis')"
                            }
                        },
                        "required": ["page_name"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "analyze_sector_performance",
                    "description": "Analyze current sector performance and identify top/bottom performers",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "time_frame": {
                                "type": "string",
                                "enum": ["1 month", "3 months", "6 months", "1 year"],
                                "description": "Time frame for sector analysis"
                            },
                            "top_n": {
                                "type": "integer",
                                "description": "Number of top and bottom performers to show",
                                "default": 3
                            }
                        },
                        "required": ["time_frame"]
                    }
                }
            }
        ]

    def chat(self, user_message, economic_context=None, conversation_history=None):
        """
        Main chat function that responds to user queries with economic context and autonomous actions.
        
        Args:
            user_message: The user's question or input
            economic_context: Dictionary containing current economic data
            conversation_history: List of previous messages for context
        
        Returns:
            Tuple: (response_text, tool_calls_list) where tool_calls_list contains actions taken
        """
        messages = [{"role": "system", "content": self.system_prompt}]
        
        # Add economic context if provided
        if economic_context:
            context_message = self._format_economic_context(economic_context)
            messages.append({
                "role": "system", 
                "content": f"Current Economic Context:\n{context_message}"
            })
        
        # Add conversation history if provided
        if conversation_history:
            messages.extend(conversation_history)
        
        # Add user message
        messages.append({"role": "user", "content": user_message})
        
        try:
            # Make initial API call with tools enabled
            response = openai.chat.completions.create(
                model=self.model,
                messages=messages,
                tools=self.tools,
                max_completion_tokens=2048
            )
            
            response_message = response.choices[0].message
            tool_calls = []
            
            # Check if the model wants to call functions
            if response_message.tool_calls:
                # Add the assistant's response to messages
                messages.append({
                    "role": "assistant",
                    "content": response_message.content,
                    "tool_calls": [
                        {
                            "id": tc.id,
                            "type": "function",
                            "function": {
                                "name": tc.function.name,
                                "arguments": tc.function.arguments
                            }
                        } for tc in response_message.tool_calls
                    ]
                })
                
                # Execute all tool calls and add results to messages
                for tool_call in response_message.tool_calls:
                    function_name = tool_call.function.name
                    function_args = json.loads(tool_call.function.arguments)
                    
                    # Execute the function and store the result
                    tool_result = self._execute_tool(function_name, function_args, economic_context)
                    tool_calls.append({
                        'name': function_name,
                        'args': function_args,
                        'result': tool_result
                    })
                    
                    # Add tool result to messages
                    messages.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": json.dumps(tool_result)
                    })
                
                # Make second API call to get final response with tool results
                final_response = openai.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    max_completion_tokens=2048
                )
                
                final_text = final_response.choices[0].message.content
                return final_text, tool_calls
            else:
                # No tool calls, just return the text response
                return response_message.content, []
                
        except Exception as e:
            return f"I encountered an error: {str(e)}. Please try again.", []

    def _format_economic_context(self, context):
        """Format economic data into a readable context string for the AI."""
        formatted = []
        
        if 'cycle_phase' in context:
            formatted.append(f"Current Business Cycle Phase: {context['cycle_phase']} ({context.get('cycle_confidence', 'N/A')}% confidence)")
        
        if 'gdp_growth' in context:
            formatted.append(f"GDP Growth: {context['gdp_growth']:.2f}%")
        
        if 'unemployment' in context:
            formatted.append(f"Unemployment Rate: {context['unemployment']:.2f}%")
        
        if 'inflation' in context:
            formatted.append(f"Inflation (CPI): {context['inflation']:.2f}%")
        
        if 'interest_rate' in context:
            formatted.append(f"Federal Funds Rate: {context['interest_rate']:.2f}%")
        
        if 'ism_manufacturing' in context:
            formatted.append(f"ISM Manufacturing PMI: {context['ism_manufacturing']:.1f}")
        
        if 'ism_services' in context:
            formatted.append(f"ISM Services PMI: {context['ism_services']:.1f}")
        
        if 'vix' in context:
            formatted.append(f"VIX (Market Volatility): {context['vix']:.2f}")
        
        if 'yield_spread' in context:
            formatted.append(f"10Y-2Y Yield Curve Spread: {context['yield_spread']:.2f} bps")
        
        if 'm2_growth' in context:
            formatted.append(f"M2 Money Supply Growth (YoY): {context['m2_growth']:.2f}%")
        
        if 'nfci' in context:
            formatted.append(f"NFCI (Financial Conditions): {context['nfci']:.2f}")
        
        if 'put_call_ratio' in context:
            formatted.append(f"Put/Call Ratio: {context['put_call_ratio']:.2f}")
        
        if 'fear_greed_index' in context:
            formatted.append(f"Fear & Greed Index: {context['fear_greed_index']:.1f} ({context.get('fear_greed_label', 'N/A')})")
        
        return "\n".join(formatted) if formatted else "No economic context available."

    def get_suggested_questions(self, cycle_phase=None):
        """Return suggested questions based on current context."""
        base_questions = [
            "What's the current VIX level?",
            "Show me the Fear & Greed Index",
            "What does the current business cycle phase mean?",
            "How should I interpret the current economic indicators?"
        ]
        
        phase_specific = {
            'Expansion': [
                "What sectors typically perform well during expansion?",
                "Show me sector performance over the last 6 months"
            ],
            'Peak': [
                "What typically happens after a peak phase?",
                "What's the current unemployment rate?"
            ],
            'Contraction': [
                "How can I protect my portfolio during contraction?",
                "Show me the current inflation rate"
            ],
            'Trough': [
                "What opportunities emerge during trough phases?",
                "What's the current ISM Manufacturing PMI?"
            ]
        }
        
        if cycle_phase and cycle_phase in phase_specific:
            return base_questions[:2] + phase_specific[cycle_phase][:2]
        
        return base_questions

    def analyze_query_intent(self, query):
        """
        Analyze the user's query to determine what kind of information they're seeking.
        This helps provide more targeted responses.
        """
        query_lower = query.lower()
        
        intent = {
            'sector_analysis': any(word in query_lower for word in ['sector', 'industry', 'rotation']),
            'business_cycle': any(word in query_lower for word in ['cycle', 'phase', 'expansion', 'contraction', 'peak', 'trough']),
            'portfolio': any(word in query_lower for word in ['portfolio', 'allocation', 'invest', 'position']),
            'indicators': any(word in query_lower for word in ['indicator', 'metric', 'data', 'ism', 'pmi', 'gdp', 'inflation']),
            'sentiment': any(word in query_lower for word in ['sentiment', 'fear', 'greed', 'vix', 'volatility']),
            'market_analysis': any(word in query_lower for word in ['market', 'stock', 'equity', 'bond', 'treasury'])
        }
        
        return intent

    def _execute_tool(self, function_name, function_args, economic_context):
        """Execute a tool/function call and return the result."""
        if function_name == "get_economic_metric":
            return self._get_economic_metric(function_args, economic_context)
        elif function_name == "create_comparison_chart":
            return self._create_comparison_chart(function_args, economic_context)
        elif function_name == "navigate_to_page":
            return self._navigate_to_page(function_args)
        elif function_name == "analyze_sector_performance":
            return self._analyze_sector_performance(function_args, economic_context)
        else:
            return {"error": f"Unknown function: {function_name}"}

    def _get_economic_metric(self, args, context):
        """Fetch a specific economic metric."""
        metric_name = args.get('metric_name')
        
        metric_map = {
            'GDP': {'key': 'gdp_growth', 'format': '.2f', 'unit': '%'},
            'Inflation': {'key': 'inflation', 'format': '.2f', 'unit': '%'},
            'Unemployment': {'key': 'unemployment', 'format': '.2f', 'unit': '%'},
            'Interest Rate': {'key': 'interest_rate', 'format': '.2f', 'unit': '%'},
            'VIX': {'key': 'vix', 'format': '.2f', 'unit': ''},
            'ISM Manufacturing': {'key': 'ism_manufacturing', 'format': '.1f', 'unit': ''},
            'ISM Services': {'key': 'ism_services', 'format': '.1f', 'unit': ''},
            'M2 Growth': {'key': 'm2_growth', 'format': '.2f', 'unit': '%'},
            'NFCI': {'key': 'nfci', 'format': '.2f', 'unit': ''},
            'Fear & Greed': {'key': 'fear_greed_index', 'format': '.1f', 'unit': ''},
            'Yield Spread': {'key': 'yield_spread', 'format': '.2f', 'unit': ' bps'},
            'Put/Call Ratio': {'key': 'put_call_ratio', 'format': '.2f', 'unit': ''}
        }
        
        if metric_name in metric_map and context:
            metric_info = metric_map[metric_name]
            key = metric_info['key']
            if key in context:
                value = context[key]
                formatted_value = f"{value:{metric_info['format']}}{metric_info['unit']}"
                return {
                    'metric': metric_name,
                    'value': formatted_value,
                    'raw_value': value,
                    'status': 'success'
                }
        
        return {'metric': metric_name, 'status': 'unavailable', 'error': 'Metric not found in context'}

    def _create_comparison_chart(self, args, context):
        """Create a comparison chart (returns chart configuration for UI to render)."""
        metrics = args.get('metrics', [])
        time_period = args.get('time_period', '1 year')
        
        return {
            'type': 'comparison_chart',
            'metrics': metrics,
            'time_period': time_period,
            'status': 'chart_requested'
        }

    def _navigate_to_page(self, args):
        """Navigate to a specific page (returns navigation instruction for UI)."""
        page_name = args.get('page_name')
        tab_name = args.get('tab_name')
        
        return {
            'type': 'navigation',
            'page': page_name,
            'tab': tab_name,
            'status': 'navigation_requested'
        }

    def _analyze_sector_performance(self, args, context):
        """Analyze sector performance (returns analysis request for data layer)."""
        time_frame = args.get('time_frame', '1 month')
        top_n = args.get('top_n', 3)
        
        return {
            'type': 'sector_analysis',
            'time_frame': time_frame,
            'top_n': top_n,
            'status': 'analysis_requested'
        }
