# 🚀 START HERE - Fitness Studio Backend API

## First Time Setup (3 Easy Steps)

### Step 1: Install Dependencies
```cmd
setup.bat
```
Wait for it to complete. Keep the terminal open!

### Step 2: Create Database & Run Migrations
```cmd
python create_database.py
python manage.py makemigrations
python manage.py migrate
python manage.py init_muscles
```

### Step 3: Start the Server
```cmd
python manage.py runserver
```

**Done!** 🎉 Access the API at: http://localhost:8000/api/docs/

---

## OR Use the All-in-One Script

```cmd
setup.bat
```
(Wait for it to finish, then in the same terminal:)

```cmd
first_run.bat
```

This does everything automatically!

---

## Got an Error?

### "Unknown database 'fitness_studio_db'"
👉 See `QUICK_FIX.md`

### "mysqlclient" compilation error
👉 Already fixed! Just run `setup.bat` again

### MySQL connection error
👉 Make sure MySQL is running:
```cmd
net start MySQL80
```

### Other issues
👉 Check `WINDOWS_SETUP.md` for Windows-specific help

---

## What's Included

- ✅ Django REST API
- ✅ JWT Authentication
- ✅ MySQL Database
- ✅ OpenAPI/Swagger Documentation
- ✅ User Management
- ✅ Exercise Tracking
- ✅ Training History & Statistics

---

## Quick Links

- **API Documentation**: http://localhost:8000/api/docs/
- **Admin Panel**: http://localhost:8000/admin/
- **Complete Guide**: `README.md`
- **Windows Setup**: `WINDOWS_SETUP.md`
- **API Testing**: `API_TESTING_GUIDE.md`

---

## Need Help?

1. Check `QUICK_FIX.md` for common errors
2. Read `WINDOWS_SETUP.md` for Windows-specific issues
3. See `README.md` for complete documentation
4. Check `SETUP_INSTRUCTIONS.md` for detailed setup

---

## Files You Need to Know

| File | Purpose |
|------|---------|
| `setup.bat` | Install dependencies |
| `create_database.py` | Create MySQL database |
| `first_run.bat` | Complete automated setup |
| `QUICK_FIX.md` | Fix common errors |
| `README.md` | Full documentation |

---

**Happy coding!** 🎉
