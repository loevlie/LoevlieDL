// Wedding Site JavaScript
// Penguin-themed interactions and enhancements

document.addEventListener('DOMContentLoaded', function() {

  // Smooth scrolling for anchor links
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
      e.preventDefault();
      const target = document.querySelector(this.getAttribute('href'));
      if (target) {
        target.scrollIntoView({
          behavior: 'smooth',
          block: 'start'
        });
      }
    });
  });

  // Subtle Easter Egg - disabled for cleaner experience
  // Can be re-enabled by uncommenting if desired

  // Add hover effect to info cards
  const cards = document.querySelectorAll('.info-card, .detail-card');
  cards.forEach(card => {
    card.addEventListener('mouseenter', function() {
      this.style.transform = 'translateY(-5px)';
    });

    card.addEventListener('mouseleave', function() {
      this.style.transform = 'translateY(0)';
    });
  });

  // RSVP form - subtle feedback removed for cleaner experience

  // Countdown timer (optional - activate if needed)
  function initCountdown() {
    const weddingDate = new Date('September 5, 2026 00:00:00').getTime();
    const countdownElement = document.getElementById('countdown');

    if (!countdownElement) return;

    const updateCountdown = () => {
      const now = new Date().getTime();
      const distance = weddingDate - now;

      const days = Math.floor(distance / (1000 * 60 * 60 * 24));
      const hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
      const minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
      const seconds = Math.floor((distance % (1000 * 60)) / 1000);

      countdownElement.innerHTML = `
        <div class="countdown-timer">
          <div class="countdown-item">
            <span class="countdown-number">${days}</span>
            <span class="countdown-label">Days</span>
          </div>
          <div class="countdown-item">
            <span class="countdown-number">${hours}</span>
            <span class="countdown-label">Hours</span>
          </div>
          <div class="countdown-item">
            <span class="countdown-number">${minutes}</span>
            <span class="countdown-label">Minutes</span>
          </div>
          <div class="countdown-item">
            <span class="countdown-number">${seconds}</span>
            <span class="countdown-label">Seconds</span>
          </div>
        </div>
      `;

      if (distance < 0) {
        countdownElement.innerHTML = "<h2>🐧💕 It's our wedding day! 💕🐧</h2>";
        clearInterval(countdownInterval);
      }
    };

    updateCountdown();
    const countdownInterval = setInterval(updateCountdown, 1000);
  }

  // Subtle parallax effect for hero section (disabled for performance)
  // Can be re-enabled if desired

  // Add animation to timeline items when they come into view
  const observerOptions = {
    threshold: 0.2,
    rootMargin: '0px 0px -50px 0px'
  };

  const observer = new IntersectionObserver(function(entries) {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.style.opacity = '1';
        entry.target.style.transform = 'translateX(0)';
      }
    });
  }, observerOptions);

  // Observe timeline items
  document.querySelectorAll('.timeline-item, .schedule-item').forEach(item => {
    item.style.opacity = '0';
    item.style.transform = 'translateX(-20px)';
    item.style.transition = 'all 0.6s ease';
    observer.observe(item);
  });

  // Form validation enhancement
  const rsvpForm = document.querySelector('.rsvp-form');
  if (rsvpForm) {
    rsvpForm.addEventListener('submit', function(e) {
      const attendance = document.querySelector('input[name="attendance"]:checked');
      if (!attendance) {
        e.preventDefault();
        alert('Please let us know if you\'ll be attending! 🐧');
        return false;
      }
    });
  }
});

// Confetti effect for successful RSVP (optional)
function launchConfetti() {
  // This could be enhanced with a confetti library like canvas-confetti
  for (let i = 0; i < 50; i++) {
    createConfettiPiece();
  }
}

function createConfettiPiece() {
  const confetti = document.createElement('div');
  confetti.textContent = ['🐧', '💕', '🎉', '✨'][Math.floor(Math.random() * 4)];
  confetti.style.position = 'fixed';
  confetti.style.left = Math.random() * 100 + '%';
  confetti.style.top = '-50px';
  confetti.style.fontSize = '1.5rem';
  confetti.style.zIndex = '9999';
  confetti.style.pointerEvents = 'none';

  document.body.appendChild(confetti);

  const fallDuration = 2000 + Math.random() * 2000;
  const sway = (Math.random() - 0.5) * 200;

  setTimeout(() => {
    confetti.style.transition = `all ${fallDuration}ms ease-in`;
    confetti.style.top = window.innerHeight + 'px';
    confetti.style.transform = `translateX(${sway}px) rotate(360deg)`;
  }, 100);

  setTimeout(() => {
    confetti.remove();
  }, fallDuration + 100);
}
