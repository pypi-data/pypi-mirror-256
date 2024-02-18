function jacobi(func, args) {
    
    // args
    // funcRoot: q_LD90, x, p
    // VT: q_LD90, qOld
    let x = args[1];
    
    var delta = 1e-8;
    let m = func(...args).length;
    let n = x.length;
    let Fp = [];
    let Fm = [];
    let J = math.zeros(m, n)._data;
    
    for(j = 0; j < n; j++)
    {
        x[j] = x[j] + delta;
        Fp = func(...args);
        
        x[j] = x[j] - 2 * delta;
        Fm = func(...args);
        
        x[j] = x[j] + delta;
        
        for(i = 0; i < m; i++)
        {
            J[i][j] = (Fp[i] - Fm[i]) / (2 * delta);
        }
    }
    
    return J;
}


function multiply(matrix, vector) { // vector-matrix-mult
    
    var coords = [];
    
    for (let i = 0; i < matrix.length; i++) {
        let dotProduct = 0;
        for (let j = 0; j < vector.length; j++) {
            dotProduct += vector[j] * matrix[i][j];
        }
        coords.push(dotProduct);
    }
    
    return coords;
}


// transformation of rotations


function changeRot(pose, func){
    
    let pos = pose.slice(0, 3);
    let rot = pose.slice(3, pose.length);
    
    rot = func(rot);
    pose = pos;
    for (let i = 0; i < rot.length; i++){
        pose.push(rot[i]);
    }
    
    return pose
}


function euler2quat(euler){
    
    const cosAlphaHalf = Math.cos(euler[0] / 2);
    const sinAlphaHalf = Math.sin(euler[0] / 2);
    const cosBetaHalf = Math.cos(euler[1] / 2);
    const sinBetaHalf = Math.sin(euler[1] / 2);
    const cosGammaHalf = Math.cos(euler[2] / 2);
    const sinGammaHalf = Math.sin(euler[2] / 2);

    const w = cosAlphaHalf * cosBetaHalf * cosGammaHalf + sinAlphaHalf * sinBetaHalf * sinGammaHalf;
    const x = sinAlphaHalf * cosBetaHalf * cosGammaHalf - cosAlphaHalf * sinBetaHalf * sinGammaHalf;
    const y = cosAlphaHalf * sinBetaHalf * cosGammaHalf + sinAlphaHalf * cosBetaHalf * sinGammaHalf;
    const z = cosAlphaHalf * cosBetaHalf * sinGammaHalf - sinAlphaHalf * sinBetaHalf * cosGammaHalf;
    
    quat = [w, x, y, z];
    
    return quat;
}


function mat2euler(T){
    
    let euler = [];
    
    var c2 = math.sqrt(T[0][0] * T[0][0] + T[1][0] * T[1][0]);
    
    if (c2 > 1e-3) {
        euler.push(math.atan2(T[2][1], T[2][2]));
        euler.push(math.atan2(-T[2][0], c2));
        euler.push(math.atan2(T[1][0], T[0][0]));
    } 
    
    else { // atan not defined
        euler.push(math.atan2(-T[1][2], T[1][1]));
        euler.push(math.atan2(-T[2][0], c2));
        euler.push(0);
    }
    
    return euler
}


function mat2quat(T){
    
    const trace = T[0][0] + T[1][1] + T[2][2];

    var w;
    var x;
    var y;
    var z;
    
    if (trace > 0) {
        const S = 0.5 / Math.sqrt(trace + 1.0);
        w = 0.25 / S;
        x = (T[2][1] - T[1][2]) * S;
        y = (T[0][2] - T[2][0]) * S;
        z = (T[1][0] - T[0][1]) * S;
    } 
    
    else if (T[0][0] > T[1][1] && T[0][0] > T[2][2]) {
        const S = 2.0 * Math.sqrt(1.0 + T[0][0] - T[1][1] - T[2][2]);
        w = (T[2][1] - T[1][2]) / S;
        x = 0.25 * S;
        y = (T[0][1] + T[1][0]) / S;
        z = (T[0][2] + T[2][0]) / S;
    } 
    
    else if (T[1][1] > T[2][2]) {
        const S = 2.0 * Math.sqrt(1.0 + T[1][1] - T[0][0] - T[2][2]);
        w = (T[0][2] - T[2][0]) / S;
        x = (T[0][1] + T[1][0]) / S;
        y = 0.25 * S;
        z = (T[1][2] + T[2][1]) / S;
    } 
    
    else {
        const S = 2.0 * Math.sqrt(1.0 + T[2][2] - T[0][0] - T[1][1]);
        w = (T[1][0] - T[0][1]) / S;
        x = (T[0][2] + T[2][0]) / S;
        y = (T[1][2] + T[2][1]) / S;
        z = 0.25 * S;
    }
    
    return [w, x, y, z];
}


function solve(A, b) {
  // Überprüfen, ob die Matrix A und der Vektor b kompatibel sind
  if (A.length !== A[0].length || A.length !== b.length) {
    throw new Error("Die Matrix und der Vektor sind nicht kompatibel.");
  }

  const n = b.length;
  const x = new Array(n).fill(0);

  // Vorwärtselimination (Gauß'sches Eliminationsverfahren)
  for (let k = 0; k < n; k++) {
    for (let i = k + 1; i < n; i++) {
      const factor = A[i][k] / A[k][k];
      b[i] -= factor * b[k];
      for (let j = k; j < n; j++) {
        A[i][j] -= factor * A[k][j];
      }
    }
  }

  // Rückwärtssubstitution
  for (let i = n - 1; i >= 0; i--) {
    let sum = 0;
    for (let j = i + 1; j < n; j++) {
      sum += A[i][j] * x[j];
    }
    x[i] = (b[i] - sum) / A[i][i];
  }

  return x;
}
