
var Engine = function(el, _MagneticField) {

  // container element object
  this.el = el[0];

  this.width = window.innerWidth;
  this.height = window.innerHeight * 1.25;

  // current date-time
  this.now = 0;

  // device capture date-time
  this.captureTime = 0;

  // array of inputs
  this.inputs = [];

  // canvas objects
  this.canvas =  null;
  this.ctx =  null;


  var deltaTop = this.el.offsetTop;
  var deltaLeft = this.el.offsetLeft;

  /**
   * input handlers..
   */
  var lastCapture = 0;
  var mouseIsDown = 0;
  var mouseId = 0;


  this.start = function() {
    run.bind(this)();
  };


  // teardown gameObject, then deallocate
  this.destroy = function() {
    this.gameObject.destroy();
    this.gameObject = null;
  };


  // call game object reseter
  this.reset = function() {
    this.gameObject.reset();
  };


  this.getImage = function() {
    return this.canvas.toDataURL();
  };



  /**
   * Private Methods
   */
  function init_canvas() {
    // create The Canvas
    this.canvas = document.createElement('canvas');
    this.canvas.width =  this.width;
    this.canvas.height =  this.height;

    // we clean the DOM
    this.el.innerHTML = '';
    // append canvas to DOM
    this.el.appendChild(this.canvas);

    // get 2d Context
    this.ctx = this.canvas.getContext('2d');
  }


  function init_game_object() {
    this.gameObject = new _MagneticField(this);
    this.gameObject.init();
  }


  function on_touch(event) {
    var inputs = [];
    for (var i = 0; i < event.targetTouches.length; ++i) {
      var type = event.type;

      if (type === 'touchstart') {
        type = 'start';
        lastCapture = 0;
      } else if (type === 'touchmove') {
        type = 'move';

        var now = new Date().getTime();

        if (lastCapture) {
          this.captureTime = lastCapture - now;
        }

        lastCapture = now;
      } else  {
        type = 'up';
        lastCapture = 0;
      }


      targetTouche = event.targetTouches[i];
      inputs.push({
        x : targetTouche.clientX - deltaLeft - window.scrollX,
        y : targetTouche.clientY - deltaTop + window.scrollY,
        id : targetTouche.identifier,
        type : type
      });
    }
    event.preventDefault();
    event.stopPropagation();
    this.inputs = inputs;
  }


  function on_mouse_down(event) {
    mouseIsDown = 1;
    lastCapture = 0;

    this.inputs = [{
      x : event.clientX - deltaLeft - window.scrollX,
      y : event.clientY - deltaTop + window.scrollY,
      id : ++mouseId,
      type : 'down'
    }];
  }


  function on_mouse_move(event) {
    if (mouseIsDown) {
      this.inputs = [{
        x : event.clientX - deltaLeft - window.scrollX,
        y : event.clientY - deltaTop + window.scrollY,
        id : mouseId,
        type : 'move'
      }];
    }

    var now = new Date().getTime();

    if (lastCapture) {
      this.captureTime = lastCapture - now;
    }
    lastCapture = now;
  }


  function on_mouse_up(event) {
    mouseIsDown = 0;
    lastCapture = 0;

    this.inputs = [{
      x : event.clientX - deltaLeft - window.scrollX,
      y : event.clientY - deltaTop + window.scrollY,
      id : mouseId,
      type : 'up'
    }];
  }


  function bind_event_listeners() {
    if ('touchstart' in window) {
      this.canvas.addEventListener('touchstart',  on_touch.bind(this));
      this.canvas.addEventListener('touchmove',   on_touch.bind(this));
      this.canvas.addEventListener('touchend',    on_touch.bind(this));
      this.canvas.addEventListener('touchleave',  on_touch.bind(this));
      this.canvas.addEventListener('touchcancel', on_touch.bind(this));
      this.canvas.addEventListener('touchenter',  on_touch.bind(this));
    }
    else {
      this.canvas.addEventListener('mousedown', on_mouse_down.bind(this));
      this.canvas.addEventListener('mousemove', on_mouse_move.bind(this));
      this.canvas.addEventListener('mouseup',   on_mouse_up.bind(this));
      this.canvas.addEventListener('mouseout',  on_mouse_up.bind(this));
    }
  }



  function run() {
    this.raf = requestAnimFrame(run.bind(this));

    // update inputs
    this.now = new Date().getTime();

    // run game..
    this.gameObject.run();
  }


  var requestAnimFrame = (function(){
    return (
      window.requestAnimationFrame       ||
      window.webkitRequestAnimationFrame ||
      window.mozRequestAnimationFrame    ||
      window.oRequestAnimationFrame      ||
      window.msRequestAnimationFrame     ||
      function(_fn, element) {
        window.setTimeout(_fn, 1000/60);
      }
   );
  })();


  // invoke initializers ..
  init_canvas.bind(this)();
  bind_event_listeners.bind(this)();
  init_game_object.bind(this)();
};




var MagnetField = function(engine) {
  /**
   * engine has the following proprieties
   * engine.width : the width of the experience
   * engine.height : the height of the experience
   * engine.ctx : the 2d context of main canvas
   * engine.canvas : the main canvas (used image saved to server!)
   * engine.inputs : an array of current input
   *                 An input is an object containing :
   *                 {x,y} : the coordinate of input
   *                 id : a unique id relative with this input (unique per 'touch')
   */
  this.engine = engine;


  var COLORS = [
    [150,85,100],
    [130,140,153],
    [55,63,75]
  ];

  // ideal to fine tune your brush
  var PARAMS = {
    squareSize: 10
  };

  var FLUIDMAP  = [];
  var PARTICLES = [];

  var WIDTH  = this.engine.width / 10 + 1 | 0;
  var HEIGHT = this.engine.width / 10 + 1 | 0;

  var ctx = engine.ctx;

  var back_canvas = document.createElement('canvas');
  back_canvas.width = this.engine.width;
  back_canvas.height = this.engine.height;
  var back_ctx = back_canvas.getContext('2d');

  var inputsDelta = {};
  var colorToId = {};
  var CURRENT_COLOR = 0;
  var getInput = false;


  /**
   * function is called after pobject is created..
   */
  this.init = function() {
    // init your experience here
    // example : we paint canvas with blue color

    this.engine.ctx.fillStyle = '#fff';
    this.engine.ctx.fillRect(0,0, this.engine.width, this.engine.height);

    for (var x = 0; x < WIDTH; ++x) {
      FLUIDMAP[x] = [];

      for (var y = 0; y < HEIGHT; ++y) {
        FLUIDMAP[x][y] = {
          x : Math.random() * 1000,
          y : Math.random() * 10
        };
      }

    }
  };

  /**
   * function is called for every frame..
   */
  this.run = function () {
    // you should manage input, render and animation here..
    // NOTE : just create functions, avoid code wall!
    // example : we run throught input and draw red squares
    this.input();
    this.animate();
    this.render();
  };

  this.input = function() {
    var $tutorial = $('#tutorial');

    for (var i=0, total=engine.inputs.length; i < total; ++i) {
      var input = engine.inputs[i];

      if (input.type !== 'up') {
        // if (!getInput) {
        //   getInput = true;
        //   $tutorial.css({display:'none'});
        // }

        if (inputsDelta[input.id]) {
          var oldInput = inputsDelta[input.id];

          var x = input.x / 20 | 0;
          var y = input.y / 20 | 0;

          var dx = (input.x - oldInput.x);
          var dy = (input.y - oldInput.y);

          if (dx >  6) {dx =  4};
          if (dx < -6) {dx = -6};
          if (dy >  6) {dy =  4};
          if (dy < -6) {dy = -6};

          FLUIDMAP[x][y].x = dx;
          FLUIDMAP[x][y].y = dy;
        }

        inputsDelta[input.id] = input;
      }
    }
  };


  this.animate = function() {
    var newFluid = [];

    if (Math.random() > .99) {
      PARTICLES.push({
        // x : Math.random() * this.engine.width,
        x : 10,
        y : 0,
        dy : 1.5,
        dx : 0
      });
    }

    if (Math.random() > .99) {
      PARTICLES.push({
        // x : Math.random() * this.engine.width,
        // y : this.engine.height,
        x : 10,
        y : 10,
        dy : -15,
        dx : 0
      });
    }

    if (Math.random() > .99) {
      PARTICLES.push({
        // y : Math.random() * this.engine.height,
        y : 0,
        x : 0,
        dy : 0,
        dx : 1.5
      });
    }

    if (Math.random() > .99) {
      PARTICLES.push({
        y : Math.random() * this.engine.height,
        x : this.engine.width,
        dy : 0,
        dx : -15
      });
    }

    if (Math.random() > .995) {
      PARTICLES.push({
        y : Math.random() * this.engine.height,
        x : this.engine.width,
        dy : -2,
        dx : 10
      });
    }

    if (Math.random() > .995) {
      PARTICLES.push({
        y : Math.random() * this.engine.height,
        x : 0,
        // x : (Math.random() * (this.engine.width / 2)),
        dy : 1.5,
        dx : 1.5
      });
    }

    if (Math.random() > .666) {
      PARTICLES.push({
        y : Math.random() * this.engine.height,
        x : Math.random() * this.engine.width,
        dy : -100,
        dx : 100
      });
    }

    if (Math.random() > .995) {
      PARTICLES.push({
        y : 0,
        x : Math.random() * this.engine.width,
        dy : 10,
        dx : 100
      });
    }


    for (var i = 0, total=PARTICLES.length; i < total; ++i) {
      var p = PARTICLES[i];

      if (!p) continue;

      // FLUIDMAP[p.x / 20 | 0][ p.y / 20 | 0].y = -p.dy / (Math.random(3) * 3);
      // FLUIDMAP[p.x / 20 | 0][ p.y / 20 | 0].x = -p.dx / (Math.random(4) * 4);

      FLUIDMAP[p.x / 210 | 0][ p.y / 20 | 0].y = -p.dy * 3;
      FLUIDMAP[p.x / 210 | 0][ p.y / 20 | 0].x = -p.dx * 4;

      p.y += p.dy;
      p.x += p.dx;

      if (
          p.y < 0 ||
          p.y >= this.engine.height ||
          p.x < 0 ||
          p.x >= this.engine.width
      ) {
        PARTICLES.splice(i--, 1);
      }
    }


    for (var x = 0; x < WIDTH; ++x) {
      newFluid[x] = [];

      for (var y = 0; y < HEIGHT; ++y) {
        // var warp = 0.15 + (Math.random(0.5) * 0.15);
        // var warp = 0.15;
        var warp = 0.13;
        var dx = FLUIDMAP[x][y].x * warp;
        var dy = FLUIDMAP[x][y].y * warp;

        if (x > 0) {
          dx += FLUIDMAP[x - 1][y].x * 0.225;
          dy += FLUIDMAP[x - 1][y].y * 0.225;
        }
        if (x < WIDTH -1) {
          dx += FLUIDMAP[x + 1][y].x * 0.225;
          dy += FLUIDMAP[x + 1][y].y * 0.225;
        }

        if (y > 0) {
          dx += FLUIDMAP[x][y - 1].x * 0.225;
          dy += FLUIDMAP[x][y - 1].y * 0.225;
        }
        if (y < HEIGHT - 1) {
          dx += FLUIDMAP[x][y + 1].x * 0.225;
          dy += FLUIDMAP[x][y + 1].y * 0.225;
        }

        if (dx >  6) {dx =  -4};
        if (dx < -6) {dx = 6};
        if (dy >  6) {dy =  6};
        if (dy < -6) {dy = -4};

        newFluid[x][y] = {
          x : dx,
          y : dy
        };

      }
    }

    FLUIDMAP = newFluid;
  }


  this.render = function() {
    back_ctx.fillStyle = '#fff';
    back_ctx.clearRect(0,0, this.engine.width, this.engine.height);
    back_ctx.globalAlpha = 1.0;
    back_ctx.strokeStyle = '#000';
    back_ctx.lineWidth = 1;


    for (var y = 0; y < HEIGHT; ++y) {
      back_ctx.beginPath();

      back_ctx.lineTo(-20 , y * 20);

      for (var x = 0; x < WIDTH; ++x) {
        var p = FLUIDMAP[x][y];
        ctx.moveTo(x * 2.0, y * 2.0);

        var _x  = .50 - Math.random(.50);
        var _y  = .50 - Math.random(.50);

        var _x  = 10;
        var _y  = .20;

        back_ctx.lineTo(
          // x * 20 + p.x * Math.random(50), y * 20 + p.y * Math.random(50) + p.x * 50);
          x * 20 + p.x * _x, y * 20 + p.y * _y + p.x * 20);
      }

      back_ctx.lineTo(
        FLUIDMAP[0].length * 20 + 20 , y * 20);
      back_ctx.stroke();
    }


    ctx.fillStyle = '#000';
    // ctx.fillStyle = '#2DEBAE';       // light blue

    var grd = ctx.createLinearGradient(0, 0, 0, this.engine.height);

    // TODO: randomize color..
    grd.addColorStop(0, '#ffffff');
    // grd.addColorStop(0, '#2DEBAE');     // light blue
    // grd.addColorStop(1, '#B0254F');  // dark blue
    grd.addColorStop(1, '#000');
    ctx.fillStyle = grd;


    ctx.fillRect(0,0, this.engine.width, this.engine.height);
    ctx.globalCompositeOperation = 'destination-in';

    ctx.drawImage(back_canvas, 0, 0);
    ctx.globalCompositeOperation = 'destination-over';

    // ctx.fillStyle = '#1C264A';
    ctx.fillStyle = '#000';
    ctx.fillRect(0,0, this.engine.width, this.engine.height);
    ctx.globalCompositeOperation = 'source-over';

  };
};


var $container = $('#container');
var engine = new Engine($container, MagnetField);
engine.start();


