<<<<<<< HEAD
# CodeAlpha_E-commerce-App
=======
# E-Commerce Store

A modern, responsive e-commerce web application built with Django, HTML, CSS (Tailwind), and JavaScript.

## Features

### Frontend
- **Responsive Design**: Mobile-first design using Tailwind CSS
- **Modern UI**: Clean, minimalist aesthetics with product-focused visuals
- **Interactive Elements**: Hover effects, animations, and smooth transitions
- **AJAX Functionality**: Seamless add-to-cart experience without page reloads
- **Search & Filters**: Advanced product filtering and search capabilities
- **Toast Notifications**: Real-time feedback for user actions

### Backend
- **Django Framework**: Robust backend with Django 4.2
- **User Authentication**: Secure registration, login, and profile management
- **Product Management**: Categories, products, and inventory tracking
- **Shopping Cart**: Session-based cart with persistent storage
- **Order Processing**: Complete checkout flow with order management
- **Admin Interface**: Comprehensive admin panel for store management

### Security
- **CSRF Protection**: Built-in Django CSRF protection
- **SQL Injection Prevention**: Django ORM protection
- **XSS Protection**: Template auto-escaping
- **Secure Forms**: Form validation and sanitization

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd ecommerce_app
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Configuration**
   ```bash
   # Copy the example environment file
   cp .env.example .env
   
   # Edit .env file and add your secret key
   # You can generate a secret key using:
   python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
   ```

5. **Database Setup**
   ```bash
   # Run migrations
   python manage.py makemigrations
   python manage.py migrate
   
   # Populate with sample data
   python manage.py populate_data
   ```

6. **Create Media Directories**
   ```bash
   mkdir media
   mkdir media/products
   mkdir media/categories
   mkdir static
   ```

7. **Run the Development Server**
   ```bash
   python manage.py runserver
   ```

8. **Access the Application**
   - Main site: http://127.0.0.1:8000/
   - Admin panel: http://127.0.0.1:8000/admin/

## Default Credentials

After running `populate_data` command:

- **Test User**: 
  - Username: `testuser`
  - Password: `testpass123`

- **Admin User**:
  - Username: `admin`
  - Password: `admin123`

## Project Structure

```
ecommerce_app/
├── ecommerce_app/          # Main project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── store/                  # Store app
│   ├── models.py          # Product, Category, Order models
│   ├── views.py           # Store views
│   ├── urls.py            # Store URLs
│   ├── admin.py           # Admin configuration
│   ├── forms.py           # Store forms
│   └── management/        # Management commands
├── accounts/              # User accounts app
│   ├── models.py          # User profile models
│   ├── views.py           # Authentication views
│   ├── forms.py           # User forms
│   └── urls.py            # Account URLs
├── templates/             # HTML templates
│   ├── base.html          # Base template
│   ├── store/             # Store templates
│   └── accounts/          # Account templates
├── static/                # Static files
│   ├── css/               # Custom CSS
│   └── js/                # JavaScript files
├── media/                 # User uploaded files
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

## Key Models

### Store Models
- **Category**: Product categories with hierarchical structure
- **Product**: Products with images, pricing, and inventory
- **Cart**: User shopping carts
- **CartItem**: Individual cart items
- **Order**: Customer orders
- **OrderItem**: Individual order items

### Account Models
- **UserProfile**: Extended user information and addresses

## API Endpoints

### Store URLs
- `/` - Product listing page
- `/product/<slug>/` - Product detail page
- `/category/<slug>/` - Category products page
- `/cart/` - Shopping cart page
- `/checkout/` - Checkout page
- `/add-to-cart/` - AJAX add to cart
- `/update-cart-item/` - AJAX update cart item
- `/remove-from-cart/` - AJAX remove from cart

### Account URLs
- `/accounts/login/` - User login
- `/accounts/register/` - User registration
- `/accounts/profile/` - User profile
- `/accounts/profile/edit/` - Edit profile
- `/accounts/orders/` - Order history
- `/accounts/logout/` - User logout

## Testing

Run the test suite:

```bash
# Run all tests
python manage.py test

# Run specific app tests
python manage.py test store
python manage.py test accounts

# Run with coverage (if installed)
coverage run --source='.' manage.py test
coverage report
```

## Performance Optimizations

- **Database Indexing**: Strategic indexes on frequently queried fields
- **Query Optimization**: Use of `select_related` and `prefetch_related`
- **Image Optimization**: Automatic image resizing on upload
- **Lazy Loading**: JavaScript-based lazy loading for images
- **Static File Optimization**: Minified CSS and JavaScript
- **Caching**: Django's caching framework ready for implementation

## Security Features

- **CSRF Protection**: Enabled on all forms
- **SQL Injection Protection**: Django ORM prevents SQL injection
- **XSS Protection**: Template auto-escaping enabled
- **Secure Headers**: Security middleware configured
- **Password Validation**: Strong password requirements
- **Session Security**: Secure session configuration

## Deployment Considerations

### Production Settings
- Set `DEBUG = False`
- Configure `ALLOWED_HOSTS`
- Use environment variables for sensitive data
- Set up proper database (PostgreSQL recommended)
- Configure static file serving (WhiteNoise included)
- Set up media file serving (AWS S3 recommended)

### Environment Variables
```
SECRET_KEY=your-secret-key
DEBUG=False
DATABASE_URL=your-database-url
ALLOWED_HOSTS=your-domain.com
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Run the test suite
6. Submit a pull request

## License

This project is licensed under the MIT License.

## Support

For support and questions, please open an issue in the repository.
>>>>>>> 631fec9 (Initial commit)
