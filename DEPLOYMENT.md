# Vercel Deployment Guide for Expense Tracker

## Pre-Deployment Setup

### 1. Repository Preparation
Ensure your GitHub repository contains:
- Root `package.json` for build configuration
- `vercel.json` for deployment configuration
- `api/` directory with Python serverless functions
- `frontend/` directory with React application

### 2. Project Structure for Vercel
```
expense-tracker/
├── package.json          # Root build configuration
├── vercel.json           # Vercel deployment config
├── api/                  # Python serverless functions
│   ├── requirements.txt  # Python dependencies
│   ├── models.py         # Database models
│   ├── schemas.py        # Pydantic schemas
│   ├── expenses.py       # POST /api/expenses
│   └── list.py          # GET /api/list
└── frontend/            # React application
    ├── package.json
    ├── src/
    └── public/
```

## Deployment Steps

### Step 1: Connect Repository to Vercel
1. Go to [vercel.com](https://vercel.com) and sign in with GitHub
2. Click "New Project"
3. Import your `expense-tracker` repository
4. Vercel will auto-detect the framework (React)

### Step 2: Configure Build Settings
Vercel should automatically detect:
- **Framework Preset**: Create React App
- **Root Directory**: `./` (leave empty)
- **Build Command**: `npm run build`
- **Output Directory**: `frontend/build`
- **Install Command**: `npm install`

### Step 3: Environment Variables (if needed)
For production database, add environment variables:
- `DATABASE_URL` - PostgreSQL connection string
- `NODE_ENV` - set to `production`

### Step 4: Deploy
1. Click "Deploy"
2. Vercel will:
   - Install dependencies
   - Build the React frontend
   - Deploy Python functions to `/api/*` routes
   - Deploy static files

## API Endpoints After Deployment

Your deployed application will have:
- **Frontend**: `https://your-app.vercel.app`
- **Create Expense**: `POST https://your-app.vercel.app/api/expenses`
- **List Expenses**: `GET https://your-app.vercel.app/api/list`

## Verification Steps

### 1. Frontend Verification
- [ ] Visit `https://your-app.vercel.app`
- [ ] Verify expense form loads
- [ ] Check that expense list displays

### 2. API Verification
Test API endpoints directly:

```bash
# Test expense creation
curl -X POST https://your-app.vercel.app/api/expenses \
  -H "Content-Type: application/json" \
  -d '{
    "idempotency_key": "test-1",
    "amount": 25.50,
    "category": "Food",
    "description": "Test expense",
    "date": "2024-01-15"
  }'

# Test expense listing
curl https://your-app.vercel.app/api/list
```

### 3. End-to-End Verification
- [ ] Create an expense through the web interface
- [ ] Verify it appears in the expense list
- [ ] Test filtering by category
- [ ] Test sorting by date
- [ ] Verify total calculation updates
- [ ] Test idempotency by refreshing after submit

### 4. Error Handling Verification
- [ ] Test with invalid data (negative amount)
- [ ] Test with missing required fields
- [ ] Verify error messages display properly

## Important Notes

### Database Limitations
- **Current Setup**: Uses SQLite in `/tmp` directory
- **Limitation**: Data doesn't persist between function invocations
- **Production Fix**: Replace with PostgreSQL or other persistent database

### Recommended Database Upgrade
For production use, update `api/models.py`:

```python
import os
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///tmp/expenses.db")
```

Then add PostgreSQL connection string to Vercel environment variables.

### Performance Considerations
- Cold starts: First request may be slower
- Function timeout: 10 seconds for Hobby plan
- Database connections: Use connection pooling for production

## Troubleshooting

### Build Failures
- Check build logs in Vercel dashboard
- Verify all dependencies in `package.json`
- Ensure Python requirements are correct

### API Errors
- Check function logs in Vercel dashboard
- Verify CORS configuration
- Test API endpoints individually

### Frontend Issues
- Check browser console for errors
- Verify API base URL configuration
- Test in incognito mode to avoid cache issues

## Rollback Plan
If deployment fails:
1. Revert to previous deployment in Vercel dashboard
2. Fix issues locally
3. Push fixes and redeploy

## Monitoring
- Use Vercel Analytics for performance monitoring
- Check function logs for errors
- Monitor API response times