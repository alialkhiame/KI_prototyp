 particlesJS("particles-js", {
      particles: {
          number: {value: 5, density: {enable: false, value_area: 800}},
          color: {value: "random"},
          shape: {
              type: "star",
              stroke: {width: 1.4, color: "#ffffff"},
              polygon: {nb_sides: 5},
              image: {src: "./images/111.jpg", width: 1, height: 100}
          },
          opacity: {
              value: 1.7,
              random: true,
              anim: {enable: false, speed: 0.8, opacity_min: 0.4, sync: false}
          },
          size: {
              value: 3.5,
              random: false,
              anim: {enable: false, speed: 40, size_min: 2.1, sync: false}
          },
          line_linked: {
              enable: false,
              distance: 100,
              color: "#a85e32",
              opacity: 1.9,
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

      update = function () {
      stats.begin();
      stats.end();


      requestAnimationFrame(update);


    };
     // Assuming you have initialized particles.js and have a way to access each particle


