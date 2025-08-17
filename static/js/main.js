// Main website functionality
document.addEventListener('DOMContentLoaded', function() {
    
    // Smooth scrolling for navigation links
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

    // Load blog posts
    loadBlogPosts();

    // Initialize contact form
    initContactForm();

    // Initialize FAQ toggles
    initFAQ();

    // Initialize mobile menu
    initMobileMenu();

    // Initialize navbar scroll effect
    initNavbarScroll();
});

function loadBlogPosts() {
    const blogContainer = document.getElementById('blogContainer');
    if (!blogContainer) return;

    fetch('/api/blogs')
        .then(response => response.json())
        .then(posts => {
            const postEntries = Object.entries(posts).slice(0, 6);
            
            if (postEntries.length === 0) {
                blogContainer.innerHTML = `
                    <div class="col-span-full text-center py-12">
                        <div class="text-gray-400 mb-4">
                            <svg class="w-16 h-16 mx-auto" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 20H5a2 2 0 01-2-2V6a2 2 0 012-2h10a2 2 0 012 2v1m2 13a2 2 0 01-2-2V7m2 13a2 2 0 002-2V9a2 2 0 00-2-2h-2m-4-3H9M7 16h6M7 8h6v4H7V8z"></path>
                            </svg>
                        </div>
                        <h3 class="text-xl font-semibold text-gray-600 mb-2">No blog posts yet</h3>
                        <p class="text-gray-500">Check back soon for our latest insights and updates.</p>
                    </div>
                `;
                return;
            }
            
            blogContainer.innerHTML = postEntries.map(([slug, post]) => 
                createBlogCard(slug, post)
            ).join('');
        })
        .catch(error => {
            console.error('Error loading blog posts:', error);
            blogContainer.innerHTML = `
                <div class="col-span-full text-center py-12">
                    <div class="text-red-400 mb-4">
                        <svg class="w-16 h-16 mx-auto" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                        </svg>
                    </div>
                    <h3 class="text-xl font-semibold text-gray-600 mb-2">Unable to load blog posts</h3>
                    <p class="text-gray-500">Please try refreshing the page.</p>
                </div>
            `;
        });
}

function createBlogCard(slug, post) {
    const categoryColors = {
        'Engineering': 'bg-blue-600',
        'Instrumentation': 'bg-green-600',
        'Environmental': 'bg-purple-600',
        'Technical': 'bg-orange-600',
        'Safety': 'bg-red-600',
        'Innovation': 'bg-indigo-600'
    };
    
    const categoryColor = categoryColors[post.category] || 'bg-gray-600';
    const imageUrl = post.image ? 
        (post.image.startsWith('/') || post.image.startsWith('http') ? post.image : 
         (post.image.includes('uploads/') ? `static/${post.image}` : `static/img/${post.image}`)) : 
        'static/img/flows.jpg';
    
    return `
        <article class="bg-white rounded-xl shadow-md overflow-hidden hover:shadow-xl transition-shadow duration-300">
            <div class="aspect-video bg-gradient-to-br from-blue-500 to-blue-700 relative">
                <img src="${imageUrl}" alt="${post.title}" class="w-full h-full object-cover" onerror="this.src='static/img/flows.jpg'">
                <div class="absolute top-4 left-4">
                    <span class="${categoryColor} text-white px-3 py-1 rounded-full text-sm font-medium">${post.category}</span>
                </div>
            </div>
            <div class="p-6">
                <div class="flex items-center text-sm text-gray-500 mb-3">
                    <time datetime="${post.date}">${formatDate(post.date)}</time>
                    <span class="mx-2">•</span>
                    <span>${post.read_time}</span>
                </div>
                <h3 class="text-xl font-bold text-gray-900 mb-3 hover:text-blue-600 transition-colors">
                    <a href="/blog/${post.id}">${post.title}</a>
                </h3>
                <p class="text-gray-600 mb-4 line-clamp-3">
                    ${post.description}
                </p>
                <a href="/blog/${post.id}" class="inline-flex items-center text-blue-600 font-semibold hover:text-blue-700 transition-colors">
                    Read More
                    <svg class="w-4 h-4 ml-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path>
                    </svg>
                </a>
            </div>
        </article>
    `;
}

function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', { 
        year: 'numeric', 
        month: 'long', 
        day: 'numeric' 
    });
}

function initContactForm() {
    const contactForm = document.getElementById('contactForm');
    
    if (contactForm) {
        contactForm.addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const submitBtn = contactForm.querySelector('button[type="submit"]');
            const originalText = submitBtn.textContent;
            
            submitBtn.textContent = 'Sending...';
            submitBtn.disabled = true;
            
            try {
                const formData = new FormData(contactForm);
                const data = {
                    name: `${formData.get('firstName')} ${formData.get('lastName')}`,
                    email: formData.get('email'),
                    subject: `${formData.get('service')} - ${formData.get('urgency')}`,
                    message: formData.get('message')
                };
                
                const response = await fetch('/contact', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/x-www-form-urlencoded',
                    },
                    body: new URLSearchParams(data)
                });
                
                const result = await response.json();
                
                if (result.success) {
                    showNotification(result.message, 'success');
                    contactForm.reset();
                } else {
                    showNotification(result.message, 'error');
                }
            } catch (error) {
                console.error('Error:', error);
                showNotification('Sorry, there was an error sending your message. Please try again.', 'error');
            } finally {
                submitBtn.textContent = originalText;
                submitBtn.disabled = false;
            }
        });
    }
}

function showNotification(message, type) {
    const notification = document.createElement('div');
    notification.className = `fixed top-4 right-4 z-50 p-4 rounded-lg shadow-lg notification ${
        type === 'success' ? 'bg-green-500 text-white' : 'bg-red-500 text-white'
    }`;
    notification.textContent = message;
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.remove();
    }, 5000);
}

function initFAQ() {
    const toggles = document.querySelectorAll('.faq-toggle');
    toggles.forEach(toggle => {
        toggle.addEventListener('click', () => {
            const target = document.getElementById(toggle.getAttribute('data-target'));
            const icon = toggle.querySelector('span');
            if (target.classList.contains('hidden')) {
                target.classList.remove('hidden');
                icon.textContent = '-';
            } else {
                target.classList.add('hidden');
                icon.textContent = '+';
            }
        });
    });
}

function initMobileMenu() {
    const btn = document.getElementById('mobile-menu-btn');
    const menu = document.getElementById('mobile-menu');
    if (!btn || !menu) return;
    
    btn.addEventListener('click', () => {
        const isHidden = menu.classList.toggle('hidden');
        btn.setAttribute('aria-expanded', String(!isHidden));
    });
    
    menu.querySelectorAll('a').forEach(a => a.addEventListener('click', () => {
        menu.classList.add('hidden');
        btn.setAttribute('aria-expanded', 'false');
    }));
}

function initNavbarScroll() {
    const navbar = document.getElementById('navbar');
    const onScroll = () => {
        if (window.scrollY > 10) {
            navbar.classList.add('nav-solid');
        } else {
            navbar.classList.remove('nav-solid');
        }
    };
    window.addEventListener('scroll', onScroll, { passive: true });
    onScroll();
}