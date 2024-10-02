import openai
import gradio as gr
import numpy as np

# Make sure to set your OpenAI API key here
openai.api_key = "YOUR_OPENAI_API_KEY"

# Define the questions to be asked in the interview
questions = [
    "Explain the concept of overfitting in machine learning and how to prevent it.",
    "How does backpropagation work in a neural network?",
    "What are some of the challenges you have faced when deploying machine learning models?"
]

# Predefined evaluation criteria and their weights
evaluation_criteria = {
    "Technical knowledge": 0.4,
    "Problem-solving ability": 0.3,
    "Communication skills": 0.2,
    "AI-related tools and techniques": 0.1
}

# Function to simulate evaluation of candidate's response
def evaluate_response(response):
    # For simplicity, we use GPT to simulate evaluation by assigning scores randomly
    evaluation_scores = {
        "Technical knowledge": np.random.uniform(0, 10),
        "Problem-solving ability": np.random.uniform(0, 10),
        "Communication skills": np.random.uniform(0, 10),
        "AI-related tools and techniques": np.random.uniform(0, 10)
    }

    total_score = sum(evaluation_scores[criterion] * weight for criterion, weight in evaluation_criteria.items())
    return evaluation_scores, total_score

# Function to conduct the interview and return the ranking
def interview_simulator(candidate_name, responses):
    candidate_results = {}
    
    for i, response in enumerate(responses):
        question = questions[i]
        evaluation_scores, total_score = evaluate_response(response)
        
        # Store candidate scores
        candidate_results[question] = {
            "response": response,
            "scores": evaluation_scores,
            "total_score": total_score
        }
    
    # Rank candidates based on total score
    overall_score = sum(result["total_score"] for result in candidate_results.values()) / len(questions)
    
    return candidate_results, overall_score

# Function to run the interview and return results
def conduct_interview(candidate_name, q1, q2, q3):
    responses = [q1, q2, q3]
    candidate_results, overall_score = interview_simulator(candidate_name, responses)
    
    # Format the output
    result_str = f"Candidate: {candidate_name}\nOverall Score: {overall_score:.2f}/10\n\n"
    for question, result in candidate_results.items():
        result_str += f"Question: {question}\nResponse: {result['response']}\n"
        result_str += "Scores:\n"
        for criterion, score in result["scores"].items():
            result_str += f"  {criterion}: {score:.2f}/10\n"
        result_str += f"Total Score for this question: {result['total_score']:.2f}/10\n\n"
    
    return result_str

# Gradio Interface
with gr.Blocks() as demo:
    gr.Markdown("### AI-Based Candidate Interview Screening System")
    
    candidate_name = gr.Textbox(label="Candidate Name")
    
    q1 = gr.Textbox(label=questions[0])
    q2 = gr.Textbox(label=questions[1])
    q3 = gr.Textbox(label=questions[2])
    
    submit_button = gr.Button("Submit Responses")
    
    result_output = gr.Textbox(label="Interview Results")
    
    submit_button.click(
        conduct_interview,
        inputs=[candidate_name, q1, q2, q3],
        outputs=[result_output]
    )

# Launch the Gradio app
demo.launch()
