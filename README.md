# Ocean City Hemp Kiosk Management System

A comprehensive self-service kiosk application for Ocean City Hemp built with Django, featuring age verification, product browsing, interactive ordering cart, special offers, budtender assistance, real-time notifications, and order finalization with receipt printing.

## Project Overview

**Goal:** Build a comprehensive self-service kiosk system that provides customers with an intuitive interface to browse and order premium cannabis products while ensuring compliance with age verification requirements.

## Technology Stack

- **Backend:** Python 3.12, Django 5.2.1
- **Database:** SQLite (development), PostgreSQL (production ready)
- **Frontend:** Django Templates, HTML5, CSS3, TailwindCSS
- **JavaScript:** Vanilla JS with real-time features and inactivity management
- **Image Handling:** Pillow with thumbnail generation
- **Environment Management:** python-dotenv
- **Testing:** Django's built-in testing framework with comprehensive coverage
- **Security:** CSRF protection, session-based authentication, form validation

## Phase 1 Implementation Status ✔

### Completed Features

1. **Project Setup**
   - ✔ Django project `OceanCityKiosk` created
   - ✔ Virtual environment configured
   - ✔ Dependencies installed and managed via `requirements.txt`
   - ✔ Environment variables configured with `.env` file
   - ✔ Static and media file handling configured

2. **Core Models**
   - ✔ `Category` model with auto-slug generation
   - ✔ `Product` model with comprehensive fields:
     - Name, description, price
     - THC/CBD content tracking
     - Flower type classification (Indica, Sativa, Hybrid, High CBD)
     - Availability status
     - Image upload support
     - Timestamps (created_at, updated_at)

3. **Django Admin Panel**
   - ✔ Category management with search and auto-populated slugs
   - ✔ Product management with:
     - List display showing key fields
     - Filtering by availability, category, and flower type
     - Search functionality
     - Bulk actions (mark available/unavailable)
     - Inline editing of price and availability

4. **Kiosk Interface**
   - ✔ Welcome screen with Ocean City Hemp branding
   - ✔ Age verification system with session management
   - ✔ Clean, professional UI with TailwindCSS styling
   - ✔ Responsive design with light-green theme
   - ✔ Message system for user feedback
   - ✔ Persistent "Call Budtender" button (placeholder)

5. **Forms & Validation**
   - ✔ Age verification form with proper validation
   - ✔ CSRF protection
   - ✔ User-friendly error handling

6. **Sample Data**
   - ✔ Management command to populate sample data
   - ✔ 5 product categories (Flower, Edibles, Concentrates, Vapes, Topicals)
   - ✔ 13 sample products with realistic data

## Phase 2 Implementation Status ✔

### Completed Features

1. **Product Browsing System**
   - ✔ Product listing with category filtering
   - ✔ Search functionality
   - ✔ Responsive grid layout
   - ✔ Product cards with images, pricing, and details
   - ✔ "Add to Cart" functionality with visual feedback

2. **Shopping Cart System**
   - ✔ Session-based cart management
   - ✔ Dynamic cart updates without page refresh
   - ✔ Quantity adjustment controls
   - ✔ Real-time price calculations
   - ✔ Cart persistence across page navigation
   - ✔ Cart item removal functionality

3. **Enhanced UI/UX**
   - ✔ Smooth animations and transitions
   - ✔ Loading states for user actions
   - ✔ Success/error notifications
   - ✔ Consistent styling across all pages

## Phase 3 Implementation Status ✔

### Completed Features

1. **Order Management System**
   - ✔ `Order` and `OrderItem` models
   - ✔ Order creation from cart contents
   - ✔ Order status tracking and management
   - ✔ Order history and details view

2. **Special Offers System**
   - ✔ `SpecialOffer` model with flexible discount types
   - ✔ Percentage and fixed amount discounts
   - ✔ Date-based offer validity
   - ✔ Category-specific offers
   - ✔ Automatic offer application in cart

3. **Budtender Assistance System**
   - ✔ `BudtenderNotification` model
   - ✔ Call budtender functionality
   - ✔ Notification status tracking
   - ✔ Budtender dashboard for managing calls

4. **Receipt & Order Finalization**
   - ✔ Professional receipt generation
   - ✔ Order summary with itemized details
   - ✔ Tax calculations and totals
   - ✔ Print-ready receipt format
   - ✔ Order completion workflow

5. **Enhanced Admin Interface**
   - ✔ Order management with search and filtering
   - ✔ Special offer administration
   - ✔ Budtender notification tracking
   - ✔ Comprehensive admin dashboards

## Phase 4 Implementation Status ✔

### Completed Features

1. **Django Admin Enhancements**
   - ✔ Product thumbnail previews in admin
   - ✔ Custom admin actions for bulk operations
   - ✔ Enhanced order inline displays
   - ✔ Date hierarchy filtering for orders
   - ✔ Improved admin list displays and filters

2. **Kiosk UI/UX Polish**
   - ✔ Real-time notification system
   - ✔ Inactivity timeout with warnings (2-minute timeout)
   - ✔ Enhanced form validation with visual feedback
   - ✔ Loading states and animations
   - ✔ Consistent user feedback across all interactions

3. **Budtender Notification Refinements**
   - ✔ Enhanced call budtender functionality with AJAX
   - ✔ Real-time notification dashboard
   - ✔ Notification timers and urgency indicators
   - ✔ Improved notification resolution system
   - ✔ Visual feedback and status updates

4. **Comprehensive Testing**
   - ✔ Model tests for all database models
   - ✔ View tests for all endpoints
   - ✔ Cart functionality tests
   - ✔ Order processing tests
   - ✔ Form validation tests
   - ✔ Security tests (CSRF, authentication, authorization)
   - ✔ Integration tests for complete workflows

5. **Security & Best Practices**
   - ✔ CSRF protection on all forms
   - ✔ Secure session management
   - ✔ Input validation and sanitization
   - ✔ Error handling and logging
   - ✔ XSS prevention measures

## Installation & Setup

### Prerequisites
- Python 3.12+
- pip package manager

### Step-by-Step Setup

1. **Clone and Setup Environment**
   ```bash
   cd /path/to/your/workspace
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Environment Configuration**
   ```bash
   # Create .env file with:
   SECRET_KEY='your-django-secret-key-here'
   DEBUG=True
   ```

3. **Database Setup**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   python manage.py createsuperuser
   ```

4. **Load Sample Data**
   ```bash
   python manage.py populate_sample_data
   ```

5. **Run Development Server**
   ```bash
   python manage.py runserver
   ```

6. **Access the Application**
   - Kiosk Interface: http://localhost:8000/
   - Admin Panel: http://localhost:8000/admin/

## Current File Structure

```
OceanCityKiosk/
├── manage.py
├── requirements.txt
├── .env
├── OceanCityKiosk/
│   ├── settings.py
│   ├── urls.py
│   └── ...
├── kiosk/
│   ├── models.py          # All models (Category, Product, Order, SpecialOffer, BudtenderNotification)
│   ├── admin.py           # Enhanced admin with thumbnails and custom actions
│   ├── views.py           # Complete kiosk workflow views
│   ├── forms.py           # Age verification and other forms
│   ├── urls.py            # URL routing for all features
│   ├── tests.py           # Comprehensive test suite
│   ├── templates/kiosk/   # HTML templates
│   │   ├── base.html      # Base template with notifications and inactivity timeout
│   │   ├── welcome.html   # Welcome screen
│   │   ├── age_verification.html  # Enhanced age verification
│   │   ├── product_list.html      # Product browsing with cart
│   │   ├── cart.html              # Shopping cart management
│   │   ├── special_offers.html    # Special offers display
│   │   ├── help.html              # Enhanced budtender call functionality
│   │   ├── budtender_dashboard.html # Real-time notification dashboard
│   │   ├── checkout.html          # Order checkout process
│   │   └── receipt.html           # Order receipt and completion
│   └── management/commands/
│       └── populate_sample_data.py
├── static/                # Static files directory
│   ├── css/
│   ├── js/
│   │   └── inactivity_timeout.js  # Inactivity management system
│   └── images/
└── mediafiles/           # Media uploads directory with product images
```

## Testing Phase 4 (Complete System)

### Functional Tests
1. **Welcome Screen & Age Verification**
   - ✔ Displays Ocean City Hemp branding
   - ✔ Age verification with enhanced feedback
   - ✔ Session management and validation
   - ✔ Smooth navigation with notifications

2. **Product Browsing & Cart**
   - ✔ Product listing with filtering and search
   - ✔ Add to cart with real-time updates
   - ✔ Cart management (add, remove, update quantities)
   - ✔ Special offer application

3. **Order Processing**
   - ✔ Checkout workflow
   - ✔ Order creation and management
   - ✔ Receipt generation and printing
   - ✔ Order completion feedback

4. **Budtender System**
   - ✔ Call budtender functionality with AJAX
   - ✔ Real-time notification dashboard
   - ✔ Notification resolution and tracking
   - ✔ Timer and urgency indicators

5. **Admin Panel**
   - ✔ Enhanced product management with thumbnails
   - ✔ Order management with filtering
   - ✔ Special offer administration
   - ✔ Budtender notification tracking

6. **UI/UX & Security**
   - ✔ Responsive design across devices
   - ✔ Inactivity timeout system
   - ✔ Real-time notifications
   - ✔ CSRF protection and secure forms
   - ✔ Input validation and error handling

### Test Coverage
- ✔ Model tests (100% coverage)
- ✔ View tests (all endpoints)
- ✔ Cart functionality tests
- ✔ Order processing tests
- ✔ Security tests
- ✔ Integration tests

Run tests with: `python manage.py test kiosk`

## Admin Credentials
- **Username:** admin
- **Email:** admin@oceancityhemp.com
- **Password:** admin123

## Next Steps (Future Enhancements)

### Potential Phase 5 Features
- **Analytics Dashboard:** Customer behavior tracking and sales analytics
- **Inventory Integration:** Real-time inventory sync with POS systems
- **Customer Loyalty:** Points system and customer accounts
- **Multi-Language Support:** Spanish language option
- **Advanced Notifications:** SMS/Email notifications for budtenders
- **Payment Integration:** Credit card processing integration
- **Reporting System:** Detailed sales and usage reports
- **API Development:** REST API for mobile app integration

## Security Notes

⚠️ **Production Deployment Checklist:**

### Current Security Features ✔
- ✔ CSRF protection on all forms
- ✔ Secure session management
- ✔ Input validation and sanitization
- ✔ XSS prevention measures
- ✔ Authentication requirements where needed

### Production Security Requirements 🔐
- [ ] Change SECRET_KEY to cryptographically strong value
- [ ] Set DEBUG=False
- [ ] Configure proper database (PostgreSQL)
- [ ] Set up HTTPS with SSL certificates
- [ ] Configure security headers (HSTS, CSP, etc.)
- [ ] Implement proper logging and monitoring
- [ ] Set up database backups
- [ ] Configure firewall and access controls
- [ ] Implement rate limiting
- [ ] Set up error monitoring (e.g., Sentry)

### Environment Variables for Production
```bash
SECRET_KEY='your-cryptographically-strong-secret-key'
DEBUG=False
DATABASE_URL='postgresql://user:password@localhost:5432/oceancityhemp'
ALLOWED_HOSTS='yourdomain.com,www.yourdomain.com'
SECURE_SSL_REDIRECT=True
SECURE_HSTS_SECONDS=31536000
```

## Support

For issues or questions regarding this kiosk system, contact the development team or refer to the Django documentation for framework-specific questions.
