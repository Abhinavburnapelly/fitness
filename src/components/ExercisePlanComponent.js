import React from 'react';

function ExercisePlanComponent({ exercisePlanData }) {
  return (
    <div>
      <h2>Exercise Plan</h2>
      {exercisePlanData["ExercisePlan"].map((exercise, index) => (
        <div key={index} style={{marginBottom: '20px'}}>
          <h3>{exercise.Exercise}</h3>
          <p><strong>Repetitions:</strong> {exercise.Repetitions}</p>
          <p><strong>Sets:</strong> {exercise.Sets}</p>
          <p><strong>Rest:</strong> {exercise.Rest}</p>
          <p><strong>Joint Angles:</strong></p>
          <ul>
            {Object.entries(exercise["Joint Angles"]).map(([joint, angle], jointIndex) => (
              <li key={jointIndex}>{joint}: {angle}</li>
            ))}
          </ul>
          <p><strong>Description:</strong> {exercise.Description}</p>
        </div>
      ))}
    </div>
  );
}

export default ExercisePlanComponent;
