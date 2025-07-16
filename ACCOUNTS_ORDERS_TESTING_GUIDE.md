# Accounts and Orders Testing Guide

## Overview
This guide provides step-by-step instructions for testing the complete accounts and orders functionality in the Kampung Cuisine application.

## Prerequisites
- Django development server running (`python manage.py runserver`)
- Database with sample products loaded
- Admin superuser account created

## Testing Checklist

### 1. User Registration Testing

#### Test New User Registration
1. Navigate to `/accounts/register/`
2. Fill out registration form:
   - Username: `testuser1`
   - Password: `testpass123`
   - Confirm Password: `testpass123`
3. Click "Register"
4. Verify:
   - ✅ User is automatically logged in
   - ✅ Redirected to products page
   - ✅ Success message appears
   - ✅ User dropdown shows in navigation
   - ✅ UserProfile automatically created

#### Test Registration Validation
1. Try registering with:
   - Existing username
   - Mismatched passwords
   - Weak password
2. Verify appropriate error messages

### 2. User Login Testing

#### Test Successful Login
1. Logout if logged in
2. Navigate to `/accounts/login/`
3. Enter valid credentials
4. Verify:
   - ✅ Successful authentication
   - ✅ Welcome message
   - ✅ Redirect to intended page
   - ✅ User menu appears

#### Test Login Validation
1. Try invalid username/password combinations
2. Verify error messages appear

### 3. Profile Testing

#### Test Profile Display
1. Login as test user
2. Navigate to `/accounts/profile/`
3. Verify profile page shows:
   - ✅ User information
   - ✅ Account statistics
   - ✅ Quick action buttons
   - ✅ Recent orders section
   - ✅ Security options

### 4. Cart and Checkout Flow Testing

#### Test Anonymous Cart
1. Logout (browse as anonymous user)
2. Add products to cart
3. Navigate to cart
4. Click "Complete Your Order"
5. Verify:
   - ✅ Redirected to login page
   - ✅ Cart items preserved after login

#### Test Authenticated Checkout
1. Login as test user
2. Add products to cart
3. Navigate to `/cart/`
4. Click "Complete Your Order"
5. Verify:
   - ✅ Redirected to checkout page
   - ✅ Form pre-filled with user data
   - ✅ Cart summary displayed

### 5. Order Placement Testing

#### Test Successful Order
1. Complete checkout form with valid data:
   ```
   Name: John Doe
   Email: john@example.com
   Phone: +60 12-345 6789
   Address: 123 Main Street, Kuala Lumpur, 50000
   Notes: Please call before delivery
   ```
2. Submit order
3. Verify:
   - ✅ Order created with unique number (KC-XXXXXXXX)
   - ✅ Cart cleared
   - ✅ Redirected to order detail page
   - ✅ Success message displayed
   - ✅ Email sent (check console/logs)

#### Test Checkout Validation
1. Try submitting with:
   - Empty required fields
   - Invalid email format
   - Short phone number
   - Short address
2. Verify validation errors

### 6. Order Management Testing

#### Test Order Detail View
1. Navigate to order detail page
2. Verify displays:
   - ✅ Order number and status
   - ✅ Customer information
   - ✅ Delivery address
   - ✅ Order items with quantities and prices
   - ✅ Total amount
   - ✅ Order timestamp

#### Test Order List
1. Navigate to `/orders/orders/`
2. Verify:
   - ✅ Lists user's orders
   - ✅ Shows order numbers, dates, status
   - ✅ Links to order details
   - ✅ Status badges displayed correctly

#### Test Order Cancellation
1. Create a new order (status: pending)
2. Go to order detail page
3. Click cancel button
4. Verify:
   - ✅ Order status changed to cancelled
   - ✅ Success message displayed
   - ✅ Cancel button no longer available

### 7. Admin Interface Testing

#### Test Order Admin
1. Login to admin (`/admin/`)
2. Navigate to Orders section
3. Verify:
   - ✅ Orders listed with status badges
   - ✅ Filtering by status works
   - ✅ Search functionality works
   - ✅ Bulk status actions available
   - ✅ Order detail shows inline items

#### Test User Profile Admin
1. Navigate to Users section
2. Edit a user
3. Verify:
   - ✅ Profile information editable inline
   - ✅ Profile auto-created for new users

### 8. Email Testing

#### Test Order Confirmation Email
1. Place a test order
2. Check email output (console for development)
3. Verify email contains:
   - ✅ Order number
   - ✅ Customer details
   - ✅ Order items and pricing
   - ✅ Delivery information
   - ✅ Contact information
   - ✅ Professional formatting

### 9. Navigation Testing

#### Test User Menu
1. Login as user
2. Verify user dropdown contains:
   - ✅ Username display
   - ✅ Profile link
   - ✅ Order history link
   - ✅ Logout link

#### Test Authentication Flow
1. Try accessing protected pages while logged out:
   - `/orders/checkout/`
   - `/orders/orders/`
   - `/accounts/profile/`
2. Verify:
   - ✅ Redirected to login
   - ✅ Redirected back after login

### 10. Error Handling Testing

#### Test Edge Cases
1. Try accessing non-existent order
2. Try cancelling delivered order
3. Try checkout with empty cart
4. Verify appropriate error messages

## Common Test Data

### Test Users
```
Username: testuser1
Password: testpass123
Email: test1@example.com

Username: testuser2  
Password: testpass123
Email: test2@example.com
```

### Test Order Data
```
Name: John Doe
Email: john@example.com
Phone: +60 12-345 6789
Address: 123 Main Street, Kuala Lumpur, 50000, Malaysia
Notes: Please call before delivery
```

## Expected Behavior

### Order Status Flow
1. **Pending** → New order placed
2. **Confirmed** → Restaurant accepted order
3. **Preparing** → Kitchen preparing food
4. **Ready** → Order ready for pickup/delivery
5. **Delivered** → Order completed
6. **Cancelled** → Order cancelled (only from pending)

### Security Checks
- Users can only view their own orders
- Checkout requires authentication
- Order cancellation only for pending orders
- CSRF protection on all forms

## Troubleshooting

### Common Issues

#### Email Not Sending
- Check console for error messages
- Verify email settings in settings.py
- Email functionality may be disabled in development

#### Forms Not Submitting
- Check for JavaScript errors in browser console
- Verify CSRF token present
- Check form validation errors

#### Order Not Creating
- Verify cart has items
- Check user authentication status
- Review server logs for errors

#### Admin Access Issues
- Ensure superuser account exists
- Check admin URL (`/admin/`)
- Verify staff/superuser permissions

## Success Criteria

✅ **All tests pass** - Users can successfully register, login, place orders, and view order history  
✅ **Admin functions work** - Restaurant staff can manage orders through admin interface  
✅ **Email notifications sent** - Order confirmations are generated  
✅ **Security measures active** - Proper authentication and authorization  
✅ **Error handling graceful** - Appropriate error messages for edge cases  

## Performance Checks

- Page load times under 2 seconds
- No database N+1 query issues
- Email sending doesn't block order creation
- Admin interface responsive with large order volumes

## Next Steps After Testing

1. **Production Deployment** - Configure for production environment
2. **Payment Integration** - Add payment gateway
3. **Email Configuration** - Setup production email service
4. **Monitoring** - Add order tracking and analytics
5. **Mobile Testing** - Verify responsive design on mobile devices

This testing guide ensures the accounts and orders functionality is working correctly and ready for production use.