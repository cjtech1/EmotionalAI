# Deployment Guide for Mind Companion Chatbot

This guide will help you deploy your mental health chatbot to a production environment once you've completed development and testing.

## 1. Prepare Your Application for Production

### Environmental Variables

Make sure all sensitive information is stored in environment variables:

- Create a `.env.production` file with production settings
- Never commit this file to version control

### Security Considerations

- Update the Flask secret key in production:
  ```python
  app.secret_key = os.environ.get('SECRET_KEY')  # Set this in your production environment
  ```
- Disable debug mode in production

### WSGI Server Setup

Flask's built-in server is not suitable for production. Use a production WSGI server like:

- Gunicorn (recommended for Linux/Mac)
- Waitress (works on Windows)

Add to requirements.txt:

```
gunicorn==20.1.0  # or waitress==2.1.2
```

## 2. Deployment Options

### Option 1: PythonAnywhere (Easiest for beginners)

1. Create an account at [PythonAnywhere](https://www.pythonanywhere.com/)
2. Upload your code via GitHub or direct upload
3. Set up a web app with Flask
4. Configure your environment variables
5. Set up a virtual environment with your dependencies

### Option 2: Heroku

1. Create a Procfile:
   ```
   web: gunicorn app:app
   ```
2. Create a runtime.txt to specify Python version:
   ```
   python-3.9.16
   ```
3. Deploy using Heroku CLI or GitHub integration

### Option 3: AWS Elastic Beanstalk

1. Install AWS EB CLI
2. Initialize your project:
   ```
   eb init
   ```
3. Create an environment:
   ```
   eb create flask-env
   ```
4. Deploy your application:
   ```
   eb deploy
   ```

## 3. Database Considerations (For Future Enhancement)

If you want to persist conversations or user data:

- Consider using SQLAlchemy with a database like PostgreSQL
- For simple needs, SQLite might be sufficient
- For cloud deployments, managed database services are recommended

## 4. Testing Before Production

- Test with production settings locally
- Verify all API keys and services work in the production environment
- Check SSL/TLS settings for secure connections

## 5. Monitoring and Maintenance

- Set up logging
- Consider implementing analytics
- Monitor API usage (especially if using OpenAI)
- Set up alerts for errors

## 6. Scale Considerations

As your chatbot grows in popularity:

- Consider rate limiting
- Add caching for common responses
- Optimize database queries if using a database
- Consider load balancing for high traffic

Remember to always follow security best practices and to keep your dependencies updated. Good luck with your deployment!
