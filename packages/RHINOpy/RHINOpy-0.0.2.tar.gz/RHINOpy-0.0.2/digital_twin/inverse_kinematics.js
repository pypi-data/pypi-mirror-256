function funcRoot_euler(q_LD90, x, p) { 
    return math.subtract(p, VT(q_LD90, x));
}

function RT_root_euler(p, q_LD90, x0){
    var x = x0;
    var F = funcRoot_euler(q_LD90, x, p);
    var eps = 1e-2;
        
    var J = [];
    var r = [];
    var dx = [];
        
    k = 0;
    while(math.norm(F, 2) > eps)
    {
        let args = [q_LD90, x, p];
        J = jacobi(funcRoot_euler, args);
        F = funcRoot_euler(q_LD90, x, p);
        r = F.map(x => -x);
    
        let J_inv = math.inv(J);
        dx = multiply(J_inv, r)
            
        x = math.add(x, dx);
            
        k = k + 1;
        if (k > 150)
        {
            VALConsole.log("break at delta x =" + math.norm(F, 2));
            return qOld;
        }
    }
        
    x[2] -= math.pi/2; // init value of axis 3
    // x = math.mod(x, 2 * math.pi);
    
    return q_LD90.concat(x);
}


function funcRoot_quat(q_LD90, x, p) { 
    return math.subtract(p, VT(q_LD90, x, 7));
}


function pseudoinv(J){ // moore_penrose

    let J_T = math.transpose(J);
    let J_inv = math.inv(math.multiply(J_T, J));
    let J_MP = math.multiply(J_inv, J_T);
    
    return J_MP;
}


function RT_root_quat(p, q_LD90, x0){
    
    p = changeRot(p, euler2quat);
    let x = x0;
    var eps = 1e-8;
    let error = 10000;

    k = 0;
    while(error > eps)
    {
        let args = [q_LD90, x, p];
        let J = jacobi(funcRoot_quat, args);
        let F = funcRoot_quat(...args);
        let J_T = math.transpose(J);
        let matrix = math.multiply(J_T, J);
        let vector = multiply(J_T, F);
        vector = vector.map(x => -x);
        let dx = solve(matrix, vector)
            
        x = math.add(x, dx);
        
        error = math.norm(multiply(J_T, F), 2);
            
        k = k + 1;
        if (k > 150)
        {
            VALConsole.log("break at delta x =" + math.norm(F, 2));
            return qOld;
        }
    }

    VALConsole.log(k)
        
    x[2] -= math.pi/2; // init value of axis 3
    
    return q_LD90.concat(x);
}


function RT_DLS(pose, q_LD90, qOld){
    
    let alpha = 0.1;
    let lambda = 0.5;
    
    let TOL = 1e-1;
    let maxIter = 150;
    
    let q = qOld;
    let F = math.norm(math.subtract(pose, VT(q_LD90, q)), 2);
    let k = 0;
    
    while (F > TOL){
        let args = [q_LD90, q];
        let J = jacobi(VT, args);
        
        let J_T = math.transpose(J);
        let LI = math.multiply(lambda * lambda, math.identity(6));
        let J_PI = math.multiply(J_T, J);
        J_PI = math.add(J_PI, LI);
        J_PI = math.inv(J_PI);
        J_PI = math.multiply(J_PI, J_T);
        
        let delta = math.subtract(pose, VT(q_LD90, q));
        let dq = math.multiply(J_PI, delta);
        let dqAlpha = math.multiply(alpha, dq);
        q = math.add(q, dqAlpha)._data;
        
        F = math.norm(delta, 2);
        k = k + 1;
        if (k > maxIter){
            VALConsole.log("Break at " + F);
            return qOld;
        }
    }
    
    q[2] -= math.pi/2; // init value of axis 3
    //q = math.mod(q, 2 * math.pi);
    
    return q_LD90.concat(q);
}


