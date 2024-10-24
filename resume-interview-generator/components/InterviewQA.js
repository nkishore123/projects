import React from 'react';

const InterviewQA = ({ questions }) => {
    return (
        <div>
            {questions.map((qa, index) => (
                <div key={index}>
                    <h4>Q: {qa.question}</h4>
                    <p>A: {qa.answer}</p>
                </div>
            ))}
        </div>
    );
};

export default InterviewQA;
