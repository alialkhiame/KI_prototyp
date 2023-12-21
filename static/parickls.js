 particlesJS("particles-js", {
      particles: {
          number: {value: 5, density: {enable: true, value_area: 200}},
          color: {value: "random"},
          shape: {
              type: "circle",
              stroke: {width: 0.3, color: "#ffffff"},
              polygon: {nb_sides: 5},
              image: {src: "./images/111.jpg", width: 1, height: 100}
          },
          opacity: {
              value: 1.7,
              random: true,
              anim: {enable: false, speed: 0.6, opacity_min: 0.4, sync: false}
          },
          size: {
              value: 4,
              random: true,
              anim: {enable: false, speed: 40, size_min: 0.1, sync: false}
          },
          line_linked: {
              enable: false,
              distance: 100,
              color: "#a85e32",
              opacity: 0.9,
              width: 2.62
          },
          move: {
              enable: true,
              speed: 6,
              direction: "none",
              random: true,
              straight: false,
              out_mode: "out",
              bounce: false,
              attract: {enable: true, rotateX: 600, rotateY: 1200}
          }
      },
      interactivity: {
          detect_on: "canvas",
          events: {
              onhover: {enable: false, mode: "grab"},

              resize: true
          },
          modes: {
              grab: {distance: 120, line_linked: {opacity: 3}},
              bubble: {distance: 400, size: 40, duration: 2, opacity: 8, speed: 3},
              repulse: {distance: 200, duration: 0.4},
              push: {particles_nb: 4},
              remove: {particles_nb: 2}
          }
      },
      retina_detect: true
      });
      var count_particles, stats, update;
      stats = new Stats();
      stats.setMode(0);
      stats.domElement.style.position = "relateive";
      stats.domElement.style.left = "0px";
      stats.domElement.style.top = "0px";
      document.body.appendChild(stats.domElement);
      count_particles = document.querySelector(".js-count-particles");
      update = function () {
      stats.begin();
      stats.end();
      if (window.pJSDom[0].pJS.particles && window.pJSDom[0].pJS.particles.array) {
          count_particles.innerText = window.pJSDom[0].pJS.particles.array.length;
      }
      updateTails();
      requestAnimationFrame(update);


    };
     // Assuming you have initialized particles.js and have a way to access each particle

// A function to create and return a tail element
function createTailElement() {
    var tail = document.createElement('div');
    tail.className = 'particle-tail';
    // Add any initial styles or attributes
    document.body.appendChild(tail); // Append to the body or a specific container
    return tail;
}

// Attach tail elements to particles
particlesJS.particles.array.forEach(particle => {
    particle.tail = createTailElement(); // Create and store the tail element
});

// Now each particle has a 'tail' property that is a DOM element
