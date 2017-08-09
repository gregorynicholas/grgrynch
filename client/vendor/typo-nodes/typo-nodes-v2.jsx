/*
 * Copyright MIT © <2013> <Francesco Trillini>
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
 * documentation files (the "Software"), to deal in the Software without restriction, including without limitation
 * the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and
 * to permit persons to whom the Software is furnished to do so, subject to the following conditions:

 * The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
 * INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR
 * PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE
 * FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
 * ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
 */


// see https://codepen.io/gregorynicholas/pen/XaWdgp


var Typo = {};


(function(Typo){

  var Typo = window.Typo || {};
  var body = document.querySelector('body');
  var canvas;
  var context;
  var mouse = {x:-99999, y:-99999};
  var nodes = [];
  var dirtyRegions = [];
  var inputForce = force = 0;
  var input = forceFactor = false;
  var FPS = 60;
  var text = 'gregory' + 'nicholas';
  var interactive = true;



  /**
   * Typo settings.
   */
  /*
  var Settings = function(){
    this.text = 'gregorynicholas';
    this.interactive = true;

    this.changeText = function(value){
      text = value;
      nodes = [], dirtyRegions = [];
      input = true;
    };

    this.enableInteractivity = function(value){
      !interactive ? interactive = true : interactive = false;
      mouse = {x:-99999, y:-99999};
    };
  };
  */


  /**
   * Typo initializer.
   */
  Typo.init = function(){

    /*
    // https://cdnjs.cloudflare.com/ajax/libs/dat-gui/0.5/dat.gui.min.js
    // Dat GUI main
    var settings = new Settings();
    var GUI = new dat.GUI();
    GUI.add(settings, 'text').onChange(settings.changeText);
    GUI.add(settings, 'interactive').onChange(settings.enableInteractivity);
    */

    this._create_canvas();

    // does the browser supports canvas?
    if (!!(Typo._support())){

      context = canvas.getContext('2d');

      this._bind_canvas();
      this._build_texture();
    }

    else {
      console.error("sorry, your browser doesn't support canvas.");
    }
  };


  /**
   * [_create_canvas description]
   * @method   _create_canvas
   * @returns  {[type]}        [description]
   */
  Typo._create_canvas = function(){
    canvas = document.createElement('canvas');
    canvas.id = 'gregorynicholas';
    canvas.width  = window.innerWidth;

    // offset the canvas to 1/3 screen height..
    canvas.height = window.innerHeight * 0.75;

    canvas.style.position = 'absolute';
    canvas.style.top = 0;
    canvas.style.bottom = 0;
    canvas.style.left = 0;
    canvas.style.right = 0;
    canvas.style.zIndex = 1001;

    // avoid hitting the dom..
    canvas._w = canvas.width;
    canvas._h = canvas.height;
    canvas._offset_top = canvas.offsetTop;
    canvas._offset_left = canvas.offsetLeft;

    // canvas.style.background = '-webkit-radial-gradient(#2bb0cc, #0079a5)';
    // canvas.style.background = '-moz-radial-gradient(#2bb0cc, #0079a5)';
    // canvas.style.background = '-ms-radial-gradient(#2bb0cc, #0079a5)';
    // canvas.style.background = '-o-radial-gradient(#2bb0cc, #0079a5)';
    // canvas.style.background = 'radial-gradient(#2bb0cc, #0079a5)';

    body.appendChild(canvas);
  };


  /**
   * [_bind_canvas description]
   * @method   _bind_canvas
   * @returns  {[type]}      [description]
   */
  Typo._bind_canvas = function(){
    var $canvas = $(canvas);
    if ('ontouchstart' in window){
      $canvas.on('touchstart', function(e){
        Typo._on_touch_start(e)
      });

      $canvas.on('touchend',   function(e){
        Typo._on_touch_end(e)
      });

      $canvas.on('touchmove',  function(e){
        Typo._on_touch_move(e)
      });

    }
    else {
      $canvas.on('mousedown', function(e){
        Typo._on_mouse_down(e);
      });

      $canvas.on('mouseup',   function(e){
        Typo._on_mouse_up(e);
      });

      $canvas.on('mousemove', function(e){
        Typo._on_mouse_move(e);
      });

    }

    $(window).on('resize', function(){
      Typo._on_window_resize();
    });
  };


  /**
   * checks if browser can support the <canvas> element
   */
  Typo._support = function(){
    return (
      canvas &&
      canvas.getContext &&
      canvas.getContext('2d'));
  };




  /**
   * window on-resize event.
   */
  Typo._on_window_resize = function(){
    canvas.width  = window.innerWidth;
    canvas.height = window.innerHeight * 0.75;

    // clear nodes, regions ..
    nodes = [];
    dirtyRegions = [];
  };

  /**
   * mouse-down event.
   */
  Typo._on_mouse_down = function(event){
    event.preventDefault();
    forceFactor = true;
  };

  /**
   * mouse-up event.
   */
  Typo._on_mouse_up = function(event){
    event.preventDefault();
    forceFactor = false;
  };

  /**
   * mouse move event.
   */
  Typo._on_mouse_move = function(event){
    event.preventDefault();
    mouse.x = event.pageX - canvas._offset_left;
    mouse.y = event.pageY - canvas._offset_top;
  };


  /**
   * touch-start event.
   */
  Typo._on_touch_start = function(event){
    event.preventDefault();
    forceFactor = true;
  };

  /**
   * touch-end event.
   */
  Typo._on_touch_end = function(event){
    event.preventDefault();
    forceFactor = false;
  };

  /**
   * touch-move event.
   */
  Typo._on_touch_move = function(event){
    event.preventDefault();
    mouse.x = event.touches[0].pageX - canvas._offset_left;
    mouse.y = event.touches[0].pageY - canvas._offset_top;
  };



  /**
   * build the canvas texture.
   */
  Typo._build_texture = function(){
    context.clearRect(0, 0, canvas._w, canvas._h);

    // start by drawing the original texture
    if (nodes.length > 0){
      Typo._build_nodes();
    }

    // logic
    Typo.clear();
    Typo.update();
    Typo.render();
    requestAnimFrame(Typo._build_texture);
  };


  Typo._build_nodes = function(){
    var _size = canvas._w / 10;
    var _step = 12;

    var _cnvs = {
      width:  canvas._w * 0.5,
      height: canvas._h * 0.5
    };

    context.font = _size + 'px "Arial"';
    // context.fillStyle = 'rgba(0, 0, 0, 1)';
    context.fillStyle = 'rgba(235, 235, 235, 1)';
    context.textAlign = 'center';
    context.fillText(text, _cnvs.width, _cnvs.height);

    var surface = context.getImageData(0, 0, canvas._w, canvas._h);

    context.clearRect(0, 0, canvas._w, canvas._h);

    for (var w = 0;     w < surface.width;   w += _step){
      for (var h = 0;   h < surface.height;  h += _step){

        var _idx = (h * surface.width * 4) + (w * 4) - 1;
        var _color = surface.data[_dx];

        // don't draw on the pixel, if not white..
        if (_color !== 255){
          continue;
        }

        var x = _cnvs.width;
        var y = _cnvs.height;

        // randomize between 1..5
        var radius = (Math.random() * 5) + 1;

        nodes.push({
          x:x, y:y,
          vx:0, vy:0,
          goalX:w, goalY:h,
          radius: radius
        });

        dirtyRegions.push({
          x:x, y:y,
          radius: radius
        });

      } // for height
    } // for width
  };


  /**
   * clears dirty regions.
   */
  Typo.clear = function(){
    [].forEach.call(dirtyRegions, function(dirty, index){
      var width = (2 * dirty.radius) + 4;
      var height = width;

      var x = dirty.x - (width / 2);
      var y = dirty.y - (height / 2);

      context.clearRect(
        Math.floor(x),
        Math.floor(y),
        Math.ceil(width),
        Math.ceil(height)
      );
    });

  };



  /**
   * updates the node-texture.
   */
  Typo.update = function(){
    var _force = 0.0001;
    var _distance = 25;

    [].forEach.call(nodes, function(node, index){
      if (!interactive){
        mouse.x = canvas.width * 0.5 + Math.sin(force) * context.measureText(text).width * 0.5;
        mouse.y = canvas.height * 0.47;
        force += _force;
      }

      var angle = Math.atan2(node.y - mouse.y, node.x - mouse.x);

      // Ease
      node.vx += Math.cos(angle) * Typo.distanceTo(mouse, node, true) + (node.goalX - node.x) * 0.1;
      node.vy += Math.sin(angle) * Typo.distanceTo(mouse, node, true) + (node.goalY - node.y) * 0.1;

      // Friction
      node.vx *= 0.7;
      node.vy *= 0.7;

      node.x += node.vx;
      node.y += node.vy;


      if (!!forceFactor){
        inputForce = Math.min(inputForce + 1, 2000);
      }
      else {
        inputForce = Math.max(inputForce - 1, 0);
      }


      // check a neighborhood node
      for (var nextMolecule = index + 1; nextMolecule < nodes.length; nextMolecule++){

        var otherMolecule = nodes[nextMolecule];

        // oh we've found one!
        if (Typo.distanceTo(node, otherMolecule) < _distance){
          context.save();
          context.beginPath();
          context.globalCompositeOperation = 'destination-over';
          context.globalAlpha = 1 - Typo.distanceTo(node, otherMolecule) / 100;
          context.lineWidth = 1;
          // context.strokeStyle = 'rgba(0,0,0, 0.8)';
          context.strokeStyle = 'rgba(255,255,255, 0.9)';
          context.moveTo(node.x, node.y);
          context.lineTo(otherMolecule.x, otherMolecule.y);
          context.stroke();
          context.closePath();
          context.restore();

        }

      }

    });

  };




  /**
   * renders the nodes.
   */
  Typo.render = function(){
    [].forEach.call(nodes, function(node, index){
      context.save();
      context.fillStyle = 'rgba(255,255,255, 0.4)';
      context.translate(node.x, node.y);
      context.beginPath();
      context.arc(0, 0, node.radius, 0, Math.PI * 2);
      context.fill();
      context.restore();

      // dirty regions
      dirtyRegions[index].x = node.x;
      dirtyRegions[index].y = node.y;
      dirtyRegions[index].radius = node.radius;
    });

  };



  /**
   * returns distance between two points.
   */
  Typo.distanceTo = function(pointA, pointB, angle){
    var dx = Math.abs(pointA.x - pointB.x);
    var dy = Math.abs(pointA.y - pointB.y);

    if (angle){
      return (1000 + (interactive ? inputForce : 0)) / Math.sqrt(dx * dx + dy * dy);
    }
    else {
      return Math.sqrt(dx * dx + dy * dy);
    }
  };



  /*
   * request new frame by Paul Irish.
   * 60 FPS.
   */
  window.requestAnimFrame = (function(){
    return (
      window.requestAnimationFrame       ||
      window.webkitRequestAnimationFrame ||
      window.mozRequestAnimationFrame    ||
      window.oRequestAnimationFrame      ||
      window.msRequestAnimationFrame     ||
      function(callback){
        window.setTimeout(callback, 1000 / FPS);
      }
    );
  })();



  $(document).ready(function(){
    console.info('Typo.init()..');
    Typo.init();
  });


})(Typo);
