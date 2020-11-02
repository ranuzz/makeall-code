(function () {

    //The `keyboard` helper function
    function keyboard(keyCode) {
        var key = {};
        key.code = keyCode;
        key.isDown = false;
        key.isUp = true;
        key.press = undefined;
        key.release = undefined;
        //The `downHandler`
        key.downHandler = event => {
            if (event.keyCode === key.code) {
            if (key.isUp && key.press) key.press();
            key.isDown = true;
            key.isUp = false;
            }
            event.preventDefault();
        };

        //The `upHandler`
        key.upHandler = event => {
            if (event.keyCode === key.code) {
            if (key.isDown && key.release) key.release();
            key.isDown = false;
            key.isUp = true;
            }
            event.preventDefault();
        };

        //Attach event listeners
        window.addEventListener(
            "keydown", key.downHandler.bind(key), false
        );
        window.addEventListener(
            "keyup", key.upHandler.bind(key), false
        );
        return key;
    }

    // The application will create a renderer using WebGL, if possible,
    // with a fallback to a canvas render. It will also setup the ticker
    // and the root stage PIXI.Container
    const app = new PIXI.Application({
        width: 512,         // default: 800
        height: 512,        // default: 600
        antialias: true,    // default: false
        transparent: false, // default: false
        resolution: 1       // default: 1
    });

    // changing background color
    app.renderer.backgroundColor = 0x061639;

    const sdim = 600;
    const tdim = 20;
    // resizing 
    app.renderer.autoResize = true;
    app.renderer.resize(sdim, sdim);

    /*
    FullScreen !!
    make sure CSS has <style>* {padding: 0; margin: 0}</style>
    app.renderer.view.style.position = "absolute";
    app.renderer.view.style.display = "block";
    app.renderer.autoResize = true;
    app.renderer.resize(window.innerWidth, window.innerHeight);
    */

    // The application will create a canvas element for you that you
    // can then insert into the DOM
    
    //document.body.appendChild(app.view);
    document.getElementById("screen").appendChild(app.view);

    rabbitTexture = new PIXI.Texture.fromImage("rabbitv3.png")
    
    const rabbits = [];
    for (let i = 0; i < (sdim/tdim); i++) {
        rabbits.push([]);
    }
    for (let i = 0; i < (sdim/tdim); i++) {
        for (let j = 0; j < (sdim/tdim); j++) {
            let cur_rabbit = new PIXI.Sprite(rabbitTexture);
            cur_rabbit.width = tdim;
            cur_rabbit.height = tdim;
            rabbits[i].push(cur_rabbit);
        }
    }
    // load the texture we need

    const board = []
    for (let i = 0; i < (sdim/tdim); i++) {
        board.push([]);
    }
    for (let i = 0; i < (sdim/tdim); i++) {
        for (let j = 0; j < (sdim/tdim); j++) {
            board[i].push(false);
        }
    }
    
    var prevx = 0;
    var prevy = 0;
    var curx = 0;
    var cury = 0;
    const dummyRabbit = new PIXI.Sprite(rabbitTexture);
    dummyRabbit.width = tdim;
    dummyRabbit.height = tdim;
    dummyRabbit.position.set(0, 0);
    app.stage.addChild(dummyRabbit);
    var startSimulation = false;

    //Capture the keyboard arrow keys
    let left = keyboard(37),
        up = keyboard(38),
        right = keyboard(39),
        down = keyboard(40);
        enter = keyboard(13);
        space = keyboard(32);
    
    enter.press = function () {
        app.stage.removeChild(dummyRabbit);
        startSimulation = true;
    };

    space.press = function () {
        if (startSimulation) {
            return;
        }
        let i = curx, j = cury;
        if (board[i][j]) {
            app.stage.removeChild(rabbits[i][j]);
        } else {
            board[i][j] = true;
            rabbits[i][j].position.set(i*tdim, j*tdim);
            app.stage.addChild(rabbits[i][j]);
        }
    };

    function placeholder() {
        if (startSimulation) return;

        if (prevx == curx && prevy == cury) return;
        
        dummyRabbit.position.set(curx*tdim, cury*tdim);
    }

    up.press = function () {
        if (startSimulation) return;
        prevx = curx;
        prevy = cury;
        if (cury > 0) {
            cury -= 1;
        }
        placeholder();
    };

    down.press = function () {
        if (startSimulation) return;
        prevx = curx;
        prevy = cury;
        if (cury < (sdim/tdim)-1) {
            cury += 1;
        }
        placeholder();
    };

    left.press = function () {
        if (startSimulation) return;
        prevx = curx;
        prevy = cury;
        if (curx > 0) {
            curx -= 1;
        }
        placeholder();
    };

    right.press = function () {
        if (startSimulation) return;
        prevx = curx;
        prevy = cury;
        if (curx < (sdim/tdim) - 1) {
            curx += 1;
        }
        placeholder();
    };

    var frame = 0;
    const frame_rate = 10;

    function cgl_loop(delta) {

        if (!startSimulation) return;

        if (frame >= frame_rate) {
            frame = 0;
        } else {
            frame += 1;
            return
        }

        let state = []
        for (let i = 0; i < (sdim/tdim); i++) {
            state.push([]);
        }
        for (let i = 0; i < (sdim/tdim); i++) {
            for (let j = 0; j < (sdim/tdim); j++) {
                state[i].push(false);
            }
        }
        let rows = (sdim/tdim);
        let cols = (sdim/tdim);
        for (let i = 0; i < (sdim/tdim); i++) {
            for (let j = 0; j < (sdim/tdim); j++) {
                let an = 0
                let cs = board[i][j]
                if (i-1 >=0 && j-1 >= 0 && board[i-1][j-1])
                    an += 1
                if (i-1 >= 0 && board[i-1][j])
                    an += 1
                if (i-1 >= 0 && j+1 < cols && board[i-1][j+1])
                    an += 1
                if (i+1 < rows && j-1 >= 0 && board[i+1][j-1])
                    an += 1
                if (i+1 < rows && board[i+1][j])
                    an += 1
                if (i+1 < rows && j+1 < cols && board[i+1][j+1])
                    an += 1
                if (j-1 >= 0 && board[i][j-1])
                    an += 1
                if (j+1 < cols && board[i][j+1] )
                    an += 1
                
                if (an < 2 && cs)
                    state[i][j] = false
                else if (an > 3 && cs)
                    state[i][j] = false
                else if (an == 3 && cs == false)
                    state[i][j] = true
                else
                    state[i][j] = board[i][j]
            }
        }
        for (let i = 0; i < (sdim/tdim); i++) {
            for (let j = 0; j < (sdim/tdim); j++) {
                if (board[i][j] != state[i][j]) {
                    if (state[i][j]) {
                        rabbits[i][j].position.set(i*tdim, j*tdim);
                        app.stage.addChild(rabbits[i][j]);
                    } else {
                        app.stage.removeChild(rabbits[i][j]);
                    }
                }
                board[i][j] = state[i][j];
            }
        }             
    }

    app.ticker.add(delta => cgl_loop(delta));
})();