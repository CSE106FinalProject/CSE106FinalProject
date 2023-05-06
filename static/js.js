function hash(str) {
    // Custom seed/"Salt" for hash function
    let seed = 58511069;

    // I'm gonna be honest idk what the rest of this function is I stole it off stack overflow
    let h1 = 0xdeadbeef ^ seed, h2 = 0x41c6ce57 ^ seed;
    for (let i = 0, ch; i < str.length; i++) {
        ch = str.charCodeAt(i);
        h1 = Math.imul(h1 ^ ch, 2654435761);
        h2 = Math.imul(h2 ^ ch, 1597334677);
    }

    h1 = Math.imul(h1 ^ (h1 >>> 16), 2246822507) ^ Math.imul(h2 ^ (h2 >>> 13), 3266489909);
    h2 = Math.imul(h2 ^ (h2 >>> 16), 2246822507) ^ Math.imul(h1 ^ (h1 >>> 13), 3266489909);

    return 4294967296 * (2097151 & h2) + (h1 >>> 0);
}

async function checkLogin() {
    // Reads username and password and assigns them to a value
    username = document.getElementById("username").value;
    password = document.getElementById("password").value;
    // Hashes password
    password = hash(password);
    console.log("test");

    // Calls the PASS function in /student as seen in index.py, assigns reply to variable data
    const response = await fetch('/login', {
        method: 'PASS',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({username, password})});
    return await response.text();
}

async function getlogin() {
    const response = await fetch('/', {method: 'GET',});
    return await response.text();
}

async function getsignup() {
    const response = await fetch('/signup', {method: 'GET',});
    return await response.text();
}

async function readLogin() {
    answer = checkLogin();

    answer.then(function(value) {
        if (value.valueOf() == "correct") {
        location.href = "home";
        }
        else document.getElementById("message").innerHTML = value;
    });
}

async function signUp() {
    // Reads username and password and assigns them to a value
    username = document.getElementById("username").value;
    password = document.getElementById("password").value;
    password1 = document.getElementById("password1").value;
    // Hashes password
    password = hash(password);
    password1 = hash(password1);
    
    // Calls the PASS function in /app as seen in index.py, assigns reply to variable data
    const response = await fetch('/signup',{
        method: 'PASS',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({username, password, password1})});
        return await response.text();
    };

async function readSignUp() {
        answer = signUp();
    
        answer.then(function(value) {
            if (value.valueOf() == "correct") {
            getlogin();
            }
            else document.getElementById("message").innerHTML = "Password Must Match";
        })
    };