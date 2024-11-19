/**
* Template Name: BizLand - v3.10.0
* Template URL: https://bootstrapmade.com/bizland-bootstrap-business-template/
* Author: BootstrapMade.com
* License: https://bootstrapmade.com/license/
*/
(function() {
  "use strict";

  /**
   * Easy selector helper function
   */
  const select = (el, all = false) => {
    el = el.trim()
    if (all) {
      return [...document.querySelectorAll(el)]
    } else {
      return document.querySelector(el)
    }
  }

  /**
   * Easy event listener function
   */
  const on = (type, el, listener, all = false) => {
    let selectEl = select(el, all)
    if (selectEl) {
      if (all) {
        selectEl.forEach(e => e.addEventListener(type, listener))
      } else {
        selectEl.addEventListener(type, listener)
      }
    }
  }

  /**
   * Easy on scroll event listener 
   */
  const onscroll = (el, listener) => {
    el.addEventListener('scroll', listener)
  }

  /**
   * Navbar links active state on scroll
   */
  let navbarlinks = select('#navbar .scrollto', true)
  const navbarlinksActive = () => {
    let position = window.scrollY + 200
    navbarlinks.forEach(navbarlink => {
      if (!navbarlink.hash) return
      let section = select(navbarlink.hash)
      if (!section) return
      if (position >= section.offsetTop && position <= (section.offsetTop + section.offsetHeight)) {
        navbarlink.classList.add('active')
      } else {
        navbarlink.classList.remove('active')
      }
    })
  }
  window.addEventListener('load', navbarlinksActive)
  onscroll(document, navbarlinksActive)

  /**
   * Scrolls to an element with header offset
   */
  const scrollto = (el) => {
    let header = select('#header')
    let offset = header.offsetHeight

    if (!header.classList.contains('header-scrolled')) {
      offset -= 16
    }

    let elementPos = select(el).offsetTop
    window.scrollTo({
      top: elementPos - offset,
      behavior: 'smooth'
    })
  }

  /**
   * Header fixed top on scroll
   */
  let selectHeader = select('#header')
  if (selectHeader) {
    let headerOffset = selectHeader.offsetTop
    let nextElement = selectHeader.nextElementSibling
    const headerFixed = () => {
      if ((headerOffset - window.scrollY) <= 0) {
        selectHeader.classList.add('fixed-top')
        nextElement.classList.add('scrolled-offset')
      } else {
        selectHeader.classList.remove('fixed-top')
        nextElement.classList.remove('scrolled-offset')
      }
    }
    window.addEventListener('load', headerFixed)
    onscroll(document, headerFixed)
  }

  /**
   * Back to top button
   */
  let backtotop = select('.back-to-top')
  if (backtotop) {
    const toggleBacktotop = () => {
      if (window.scrollY > 100) {
        backtotop.classList.add('active')
      } else {
        backtotop.classList.remove('active')
      }
    }
    window.addEventListener('load', toggleBacktotop)
    onscroll(document, toggleBacktotop)
  }

  /**
   * Mobile nav toggle
   */
  on('click', '.mobile-nav-toggle', function(e) {
    select('#navbar').classList.toggle('navbar-mobile')
    this.classList.toggle('bi-list')
    this.classList.toggle('bi-x')
  })

  /**
   * Mobile nav dropdowns activate
   */
  on('click', '.navbar .dropdown > a', function(e) {
    if (select('#navbar').classList.contains('navbar-mobile')) {
      e.preventDefault()
      this.nextElementSibling.classList.toggle('dropdown-active')
    }
  }, true)

  /**
   * Scrool with ofset on links with a class name .scrollto
   */
  on('click', '.scrollto', function(e) {
    if (select(this.hash)) {
      e.preventDefault()

      let navbar = select('#navbar')
      if (navbar.classList.contains('navbar-mobile')) {
        navbar.classList.remove('navbar-mobile')
        let navbarToggle = select('.mobile-nav-toggle')
        navbarToggle.classList.toggle('bi-list')
        navbarToggle.classList.toggle('bi-x')
      }
      scrollto(this.hash)
    }
  }, true)

  /**
   * Scroll with ofset on page load with hash links in the url
   */
  window.addEventListener('load', () => {
    if (window.location.hash) {
      if (select(window.location.hash)) {
        scrollto(window.location.hash)
      }
    }
  });

  /**
   * Preloader
   */
  let preloader = select('#preloader');
  if (preloader) {
    window.addEventListener('load', () => {
      preloader.remove()
    });
  }

  /**
   * Initiate glightbox
   */
  const glightbox = GLightbox({
    selector: '.glightbox'
  });

  /**
   * Skills animation
   */
  let skilsContent = select('.skills-content');
  if (skilsContent) {
    new Waypoint({
      element: skilsContent,
      offset: '80%',
      handler: function(direction) {
        let progress = select('.progress .progress-bar', true);
        progress.forEach((el) => {
          el.style.width = el.getAttribute('aria-valuenow') + '%'
        });
      }
    })
  }

  /**
   * Testimonials slider
   */
  new Swiper('.testimonials-slider', {
    speed: 600,
    loop: true,
    autoplay: {
      delay: 5000,
      disableOnInteraction: false
    },
    slidesPerView: 'auto',
    pagination: {
      el: '.swiper-pagination',
      type: 'bullets',
      clickable: true
    }
  });

  /**
   * Porfolio isotope and filter
   */
  window.addEventListener('load', () => {
    let portfolioContainer = select('.portfolio-container');
    if (portfolioContainer) {
      let portfolioIsotope = new Isotope(portfolioContainer, {
        itemSelector: '.portfolio-item'
      });

      let portfolioFilters = select('#portfolio-flters li', true);

      on('click', '#portfolio-flters li', function(e) {
        e.preventDefault();
        portfolioFilters.forEach(function(el) {
          el.classList.remove('filter-active');
        });
        this.classList.add('filter-active');

        portfolioIsotope.arrange({
          filter: this.getAttribute('data-filter')
        });
        portfolioIsotope.on('arrangeComplete', function() {
          AOS.refresh()
        });
      }, true);
    }

  });

  /**
   * Initiate portfolio lightbox 
   */
  const portfolioLightbox = GLightbox({
    selector: '.portfolio-lightbox'
  });

  /**
   * Portfolio details slider
   */
  new Swiper('.portfolio-details-slider', {
    speed: 400,
    loop: true,
    autoplay: {
      delay: 5000,
      disableOnInteraction: false
    },
    pagination: {
      el: '.swiper-pagination',
      type: 'bullets',
      clickable: true
    }
  });

  /**
   * Animation on scroll
   */
  window.addEventListener('load', () => {
    AOS.init({
      duration: 1000,
      easing: 'ease-in-out',
      once: true,
      mirror: false
    })
  });

  /**
   * To show user's email instead of Login and Register button
   */
  document.addEventListener('DOMContentLoaded', () => {
    const accessToken = sessionStorage.getItem('accessToken');
    const email = sessionStorage.getItem('email');
    if (accessToken && email) {
      const registerButtons = document.querySelector('.register-buttons');
      const userEmailElement = document.createElement('div');
      userEmailElement.classList.add('nav-item', 'dropdown');
      userEmailElement.innerHTML = `
          <a class="nav-link dropdown-toggle" href="#" id="userDropdown" role="button" data-bs-toggle="dropdown" aria-expanded="false">
            ${email}
          </a>
          <ul class="dropdown-menu" aria-labelledby="userDropdown">
            <li><a class="dropdown-item" href="profile.html">Profile</a></li>
            <li><a class="dropdown-item" href="#" id="logout">Logout</a></li>
          </ul>
        `;
      // userEmailElement.innerHTML = `<a href="profile.html" class="nav-link scrollto">${email}</a>`;
      registerButtons.parentNode.replaceChild(userEmailElement, registerButtons);

      // Add logout functionality
      document.getElementById('logout').addEventListener('click', () => {
        sessionStorage.removeItem('accessToken');
        sessionStorage.removeItem('userEmail');
        window.location.href = 'index.html';
      });

      // Hide the register button in the hero section
      const heroRegisterButton = document.querySelector('.btn-register');
      if (heroRegisterButton) {
        heroRegisterButton.style.display = 'none';
      }
    }
  });

  /**
   * Initiate Pure Counter 
   */
  new PureCounter();

})()

baseURL = "https://diabetes-umass-backend.onrender.com"

async function login(event) {
  event.preventDefault();

  const email = document.getElementById('login_email').value;
  const password = document.getElementById('login_password').value;
  const loginData = { email, password };
  const url = baseURL + '/login'

  try {
      const response = await fetch(url, {
          method: 'POST',
          headers: {
              'Content-Type': 'application/json'
          },
          body: JSON.stringify(loginData)
      });

      if (!response.ok) {
          document.getElementById('login-error').innerText = 'Check your Email and Password';
          return;
      }

      const data = await response.json();
      // Store access token in session/local storage
      sessionStorage.setItem('accessToken', data.access_token);
      sessionStorage.setItem('email', email);
      sessionStorage.setItem('userId', data.user_id);

      // Redirect to the home page
      window.location.href = 'index.html';
  } catch (error) {
      console.error('There has been a problem with your fetch operation:', error);
  }
}

async function register(event) {
  event.preventDefault();

  const full_name = document.getElementById('fullname').value;
  const email = document.getElementById('email').value;
  const password = document.getElementById('password').value;
  const registerData = { full_name, email, password };
  const url = baseURL + '/register'

  try {
      const response = await fetch(url, {
          method: 'POST',
          headers: {
              'Content-Type': 'application/json'
          },
          body: JSON.stringify(registerData)
      });

      message = document.getElementById('register-message');
      error = document.getElementById('register-error')

      if (!response.ok) {
        message.style.display = "none";
        error.style.display = "block";
        error.innerText = 'User is already registered';
          return;
      }

      const data = await response.json();
      
      error.style.display = "none";
      message.style.display = "block";
      message.innerText = 'User is registered! You can login to continue.';
  } catch (error) {
      console.error('There has been a problem with your fetch operation:', error);
  }
}

async function get_chat_response(event) {
  event.preventDefault();

  const chatForm = document.getElementById('chatForm');
  const chatMessages = document.getElementById('chatMessages');
  const userMessageInput = document.getElementById('userMessage');
  const userMessage = userMessageInput.value.trim();

  const url = baseURL + '/chat';
  const accessToken = sessionStorage.getItem('accessToken');

  if (!accessToken){
    addMessageToChat('bot', 'Login to access the chatbot!');
    return;
  }

  if (userMessage) {
    addMessageToChat('user', userMessage);
    userMessageInput.value = '';
    
    try {
      const response = await fetch(url, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': 'Bearer ' + accessToken,
        },
        body: JSON.stringify({ query: userMessage }),
      });

      const data = await response.json();
      if (data && data.response) {
        addMessageToChat('bot', data.response);
      } else {
        addMessageToChat('bot', 'Sorry, I could not understand that.');
      }
    } catch (error) {
      console.error('Error:', error);
      addMessageToChat('bot', 'There was an error processing your request.');
    }
  }

  function addMessageToChat(sender, message) {
    const messageElement = document.createElement('div');
    messageElement.classList.add('d-flex', 'flex-row', 'p-3');
    
    if (sender === 'user') {
      messageElement.innerHTML = `
        <div class="bg-white mr-2 p-3"><span class="text-muted">${message}</span></div>
        <img src="https://img.icons8.com/color/48/000000/circled-user-male-skin-type-7.png" width="30" height="30">
      `;
    } else {
      messageElement.innerHTML = `
        <img src="https://img.icons8.com/color/48/000000/circled-user-female-skin-type-7.png" width="30" height="30">
        <div class="bg-white ml-2 p-3"><span class="text-muted">${message}</span></div>
      `;
    }
    
    chatMessages.appendChild(messageElement);
    chatMessages.scrollTop = chatMessages.scrollHeight;
  }
}

