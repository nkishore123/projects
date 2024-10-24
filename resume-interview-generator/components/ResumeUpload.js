import React, { useState } from 'react';
import { generateQuestionsAndAnswers } from '../OpenAI'; // Correctly import as a named export

const ResumeUpload = () => {
    const [questions, setQuestions] = useState([]);
    const [error, setError] = useState('');
    const [resumeText, setResumeText] = useState('');
    const [loading, setLoading] = useState(false);

    const handleUpload = (event) => {
        const file = event.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = (e) => {
                setResumeText(e.target.result);
                setError('');
            };
            reader.readAsText(file);
        } else {
            setError('Please upload a valid resume file.');
        }
    };

    const handleGenerate = async () => {
        if (!resumeText) {
            setError('Please upload a resume before generating questions.');
            return;
        }
        setLoading(true);
        setError(''); // Clear any previous errors
        try {
            const result = await generateQuestionsAndAnswers(resumeText);
            setQuestions(result.questions);
        } catch (err) {
            setError('Error generating questions. Please try again.');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="resume-upload">
            <input type="file" accept=".txt,.pdf" onChange={handleUpload} />
            <button onClick={handleGenerate} disabled={loading}>
                {loading ? 'Generating...' : 'Generate Questions'}
            </button>
            {error && <p className="error">{error}</p>}
            <div className="qa-list">
                {questions.map((qa, index) => (
                    <div key={index} className="qa-item">
                        <h4>Q: {qa.question}</h4>
                        <p>A: {qa.answer}</p>
                    </div>
                ))}
            </div>
        </div>
    );
};

export default ResumeUpload;
