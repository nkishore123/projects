import axios from 'axios';

const API_URL = 'https://api.openai.com/v1/chat/completions';

export const generateQuestionsAndAnswers = async (resumeText) => {
    const apiKey = process.env.REACT_APP_OPENAI_API_KEY; 

    const response = await axios.post(
        API_URL,
        {
            model: 'gpt-3.5-turbo',
            messages: [
                {
                    role: 'system',
                    content: `You are a highly experienced technical interviewer with over 10 years of experience in the industry. Based on the resume provided, generate technical interview questions and provide thoughtful, well-structured answers as you would in a real technical interview. Focus on both technical and problem-solving skills relevant to the candidate's experience.`,
                },
                {
                    role: 'user',
                    content: `Here is the candidate's resume:\n\n${resumeText}\n\nPlease generate 10 interview questions along with suggested answers.`,
                },
            ],
        },
        {
            headers: {
                'Content-Type': 'application/json',
                Authorization: `Bearer ${apiKey}`,
            },
        }
    );

    const completionText = response.data.choices[0].message.content;

    const qaList = completionText
        .split('\n')
        .filter((line) => line.includes('Q:')) 
        .map((line) => {
            const [question, answer] = line.split('A:');
            return {
                question: question.replace('Q:', '').trim(),
                answer: answer?.trim() || 'No answer provided',
            };
        });

    return { questions: qaList };
};
