function DH(theta, d, a, alpha) {
    
    let A_i = [[math.cos(theta), -math.sin(theta) * math.cos(alpha), math.sin(theta) * math.sin(alpha),  a * math.cos(theta)],
               [math.sin(theta), math.cos(theta) * math.cos(alpha),  -math.cos(theta) * math.sin(alpha), a * math.sin(theta)],
               [0,               math.sin(alpha),                    math.cos(alpha),                    d],
               [0,               0,                                  0,                                  1]];
    
    return A_i
}


function VT(q_LD90, q_TM5, N=6) {
    
    // model parameters
    let h_LD90 = 833; 
    let theta = [q_TM5[0], q_TM5[1] - math.pi/2, q_TM5[2], q_TM5[3] + math.pi/2, q_TM5[4], q_TM5[5]];
    let d =     [145.2, 146, -129.7, 106, 106, 113.2];
    let a =     [0, 429, 411.5, 0, 0, 0];
    let alpha = [-math.pi/2, 0, 0, math.pi/2, -math.pi/2, 0];
    
    // DH-matrices
    /*let T = [[math.cos(q_LD90[2]),  0, math.sin(q_LD90[2]), q_LD90[0]],
             [0,                    1, 0,                   q_LD90[1]],
             [-math.sin(q_LD90[2]), 0, math.cos(q_LD90[2]), h_LD90],
             [0,                    0, 0,                   1]]; 
        // DH-matrix for the LD90*/
             
    let T =  [[1,0,0,0],
              [0,1,0,0],
              [0,0,1,0],
              [0,0,0,1]];
    
    for (let i = 0; i < 6; i++) { // transformation from C0 to Cn
        T = math.multiply(T, DH(theta[i], d[i], a[i], alpha[i])); 
    }

    // Coord transformation
    var coords = multiply(T, [0, 0, 0, 1]);
    
    // Build pose vector
    let pose = [];

    // coordinates
    for (let i = 0; i < 3; i++){
        pose.push(coords[i]);
    }
    
    if (N === 6){ // euler angles
        euler = mat2euler(T);
        for (let i = 0; i < 3; i++){
            pose.push(euler[i]);
        }
    }
    
    else {
        quat = mat2quat(T);
        for (let i = 0; i < 4; i++){
            pose.push(quat[i]);
        }
    }
    
    return pose;
}
