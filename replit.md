# Overview

This is a Telegram bot-based shop system built with Python and Aiogram 3.x that enables automated cryptocurrency and fiat payment processing for digital goods sales, specifically optimized for **Telegram Stars purchases** with configurable markup. The bot supports multiple payment methods (QIWI, YooMoney, CryptoBot), automated inventory management, user transactions, administrative controls, **promocode system with bonus balance**, and **mandatory channel subscription**. It's designed as a complete e-commerce solution within Telegram's messaging platform.

## Recent Changes (2025-10-23)

### Promocode System
- ✅ **Bonus Balance**: Added separate bonus balance for users (can only be used for purchasing products, not stars)
- ✅ **Promocode Creation**: Admin panel for creating promocodes with configurable amounts and usage limits
- ✅ **Usage Options**: Support for single-use, limited-use (5, 10), and unlimited promocodes
- ✅ **User Activation**: Users can activate promocodes via "🎟️ Промокод" button
- ✅ **Admin Notifications**: Automatic notifications to admins when promocodes are activated
- ✅ **Promocode Management**: View all promocodes, usage statistics, and delete promocodes
- ✅ **Database Tables**: Added `storage_promocodes` and `storage_promocode_usage` tables

### Channel Integration
- ✅ **Games Channel Button**: Added "🎮 Игры на звезды" button with configurable URL in settings.ini
- ✅ **Free Gifts Channel Button**: Added "🎁 Бесплатные подарки и звезды" button with configurable URL
- ✅ **Configuration**: New settings: `games_url` and `free_gifts_url` in settings.ini

### Mandatory Subscription System
- ✅ **Subscription Middleware**: Added middleware to check user subscription status
- ✅ **Multi-Channel Support**: Support for up to 5 required channels/chats
- ✅ **Smart Link Generation**: Automatic invite link creation for private channels
- ✅ **Admin Bypass**: Administrators automatically bypass subscription checks
- ✅ **Configuration**: `required_channels` parameter in settings.ini

### User Profile Enhancements
- ✅ **Bonus Balance Display**: Shows bonus balance in user profile when > 0
- ✅ **Clear Indicators**: Bonus balance marked as "только для покупки товаров"
- ✅ **Admin View**: Bonus balance visible in admin user profile view

### Database Updates
- Added `user_bonus_balance` field to `storage_users` table with automatic migration
- Created `storage_promocodes` table with fields: promocode, balance, usage_count, max_usage, created_by, created_unix
- Created `storage_promocode_usage` table for tracking individual activations

## Recent Changes (2025-10-22)

### User Interface Enhancements
- ✅ **Chat Button**: Added configurable "💬 Чат" button in main menu
  - New `chat_url` setting in `settings.ini` (supports @username or full URL)
  - Button appears only when chat_url is configured
  - Intelligent link formatting (detects @handles vs full URLs)
  - Handler: `user_menu.chat_link_finl` with inline keyboard

- ✅ **Enhanced Welcome Menu**: Redesigned greeting with emoji animations
  - Multi-line welcome text with visual appeal
  - Emoji sequence: 🎉 👋 🛍️ 💎 ⭐ 🎁
  - Improved user onboarding experience
  - Updated in `main_start.py`

### Admin Tools
- ✅ **User Export**: CSV export functionality in statistics panel
  - New "📥 Экспорт пользователей" button in admin statistics
  - Exports: user_id, username, name, balance, total refills, total given, registration date
  - UTF-8 BOM encoding for Excel compatibility
  - Handler: `admin_functions.admin_export_users`
  - File format: `users_export_<timestamp>.csv`

### System Verification
- ✅ **CryptoBot Balance Top-up**: Verified existing implementation (no changes needed)
  - Payment flow already functional (lines 93-102 in user_transactions.py)
  - Supports CryptoBot cryptocurrency payments
  - Invoice creation and payment verification working correctly

### Configuration
- Added `chat_url` parameter to Settings section in `settings.ini`
- New function: `get_chat_url()` in `config.py` for safe config reading
- Cleaned up `requirements.txt` (removed duplicates)

### Code Quality
- Architect review: **Pass** - all features functional, no regressions
- Bot successfully starts with "BOT WAS STARTED" confirmation
- All existing features preserved (QIWI, YooMoney, CryptoBot, Stars purchases, middleware, schedulers)

## Previous Changes (2025-10-21)

### Critical Security Fixes
- ✅ **Fixed payment amount exploit**: Total amount now recalculated on server side, preventing client-side price manipulation
- ✅ **Server-side validation**: All payment amounts verified using `amount_stars * STAR_RATE * (1 + markup/100)` formula
- ✅ **Database schema alignment**: Fixed StarsPurchasex.add calls to use correct field names (purchase_receipt, purchase_unix, recipient_username)

### Stars Purchase System
- ✅ Added dual payment options: CryptoBot invoice or bot balance
- ✅ Implemented `credit_stars_to_recipient()` function for automatic star delivery
- ✅ Full FSM flow: select amount → choose recipient (self/friend) → payment method → delivery
- ✅ Minimum 50 stars, pricing at $0.018/star + configurable admin markup
- ✅ Balance refund on errors (recipient not found, insufficient funds)
- ✅ Admin notifications for all star purchases

### Refill System Improvements
- ✅ Added cancel button during balance refill amount input
- ✅ Improved UX with `refill_cancel_finl()` inline keyboard

### Database Updates
- Added `storage_stars_purchases` table with fields: user_id, recipient_id, recipient_username, amount_stars, amount_paid, markup_percent, purchase_receipt, purchase_unix
- Added `stars_markup` field to `storage_settings` table (default: 10%)
- Automatic migration for existing databases

### New Features
- **Stars Purchase Menu**: Users can buy stars via "⭐ Купить звезды" button
- **Gift Stars**: Send stars to friends by entering their Telegram username
- **Dual Payment**: Choose between CryptoBot cryptocurrency or bot balance
- **Transparent Pricing**: Base amount, markup %, and total displayed before payment
- **Admin Controls**: `⚙️ Настройки` → `⭐ Наценка на звезды` (0-100%)

### Documentation
- Created comprehensive `STARS_SETUP.md` with setup instructions
- Updated `CRYPTOBOT_SETUP.md` with Stars integration details
- Added `.gitignore` for Python project best practices

# User Preferences

Preferred communication style: Simple, everyday language.

# System Architecture

## Core Framework & Bot Implementation

**Problem:** Need a robust, asynchronous Telegram bot framework for handling e-commerce operations  
**Solution:** Aiogram 3.2.0 with async/await patterns throughout  
**Rationale:** Aiogram 3.x provides modern async support, built-in FSM (Finite State Machine) for conversational flows, and clean middleware architecture. The async nature allows handling multiple payment checks and user interactions concurrently without blocking.

## Database Architecture

**Problem:** Persistent storage for users, products, transactions, and settings  
**Solution:** SQLite with custom ORM-like wrapper using Pydantic models  
**Rationale:** 
- SQLite provides zero-configuration embedded database
- Pydantic models ensure type safety and validation
- Custom wrapper (`db_helper.py`) provides clean abstraction over raw SQL
- Separate model files for each entity (users, categories, positions, items, purchases, refills, payments, settings)

**Schema Design:**
- `storage_users` - User profiles and balances
- `storage_category` - Product categories hierarchy
- `storage_position` - Product listings with pricing
- `storage_item` - Individual inventory items (sold separately)
- `storage_purchases` - Purchase history and receipts
- `storage_refill` - Balance top-up transactions
- `storage_payment` - Payment gateway credentials
- `storage_settings` - Bot configuration and feature toggles

## Payment Gateway Integrations

**Problem:** Accept multiple payment methods with different APIs  
**Solution:** Abstracted payment service layer with dedicated API classes

**Payment Processors:**
1. **QIWI Wallet** (`api_qiwi.py`)
   - API-based payment verification
   - Balance checking
   - Transaction history

2. **YooMoney** (`api_yoomoney.py`)
   - OAuth token authentication
   - Payment link generation
   - Status polling

3. **CryptoBot** (`api_cryptobot.py`)
   - Cryptocurrency payments (BTC, ETH, USDT, TON)
   - Invoice creation via Crypto Pay API
   - Real-time payment verification

**Design Pattern:** Each payment class follows similar interface:
- Token/credentials management
- Balance checking methods
- Payment creation
- Status verification
- Error handling with admin notifications

## State Management

**Problem:** Multi-step user interactions (product selection, payment flow, admin operations)  
**Solution:** Aiogram FSM (Finite State Machine) with custom state handling  
**Implementation:**
- States stored in `FSMContext`
- State data persisted across handler calls
- Clear state transitions for different workflows
- Automatic state cleanup on completion

## Middleware Architecture

**Anti-Spam Protection** (`middleware_throttling.py`):
- TTL-based cache (10,000 users, 10-minute expiry)
- Dynamic rate limiting with progressive delays
- Per-user throttling counters

**User Management** (`middleware_users.py`):
- Automatic user registration on first interaction
- Profile updates (username, display name)
- HTML sanitization for user inputs

## Routing & Handler Organization

**Structure:**
- Separate routers for admin and user functionality
- Admin routes protected by `IsAdmin` filter
- Feature-based route grouping:
  - `admin_menu.py` - Admin dashboard
  - `admin_payment.py` - Payment system configuration
  - `admin_products.py` - Inventory management
  - `user_menu.py` - User interface
  - `user_transactions.py` - Payment processing

## Scheduled Tasks

**Problem:** Automated maintenance and statistics  
**Solution:** APScheduler with cron-based jobs  
**Jobs:**
- Daily profit reporting (00:00:15)
- Weekly statistics reset (Monday 00:00:10)
- Monthly counter updates (1st day 00:00:05)
- Automatic database backups (daily 00:00)
- Update checks (daily 00:00)
- Email notifications (daily 12:00)

## Keyboard System

**Two-Layer Interface:**
1. **Reply Keyboards** (`reply_main.py`)
   - Main menu navigation
   - Context-aware buttons (admin vs user)
   - Payment system selection

2. **Inline Keyboards** (`inline_*.py`)
   - Paginated product browsing
   - Payment confirmation
   - Admin controls
   - Dynamic callback data with state preservation

**Pagination Pattern:**
- 10 items per page
- Forward/backward navigation
- Jump to first/last page
- State preservation via callback data

## Error Handling & Logging

**Logging System:**
- Dual output: file (`logs.log`) + colored console
- Structured format with timestamps, file locations, line numbers
- Exception tracking in error handlers

**Error Recovery:**
- Telegram API error suppression (message edit conflicts)
- Payment gateway failure notifications to admins
- Graceful degradation for missing data

## Security Considerations

**Input Sanitization:**
- HTML tag stripping for user-generated content
- SQL injection prevention via parameterized queries
- Admin-only access controls

**Credential Storage:**
- Payment tokens stored in database
- No hardcoded secrets
- Token validation before enabling payment methods

# External Dependencies

## Payment Gateways

**QIWI Wallet API**
- Purpose: Russian payment system integration
- Authentication: API token + phone number
- Features: Balance checking, payment verification

**YooMoney API**
- Purpose: Russian digital wallet payments
- Authentication: Bearer token (OAuth)
- Endpoint: `https://yoomoney.ru/api/`

**CryptoBot (Crypto Pay API)**
- Purpose: Cryptocurrency payment processing
- Authentication: API token header (`Crypto-Pay-API-Token`)
- Endpoint: `https://pay.crypt.bot/api/`
- Supported currencies: BTC, ETH, USDT, TON, and others

## Core Libraries

**Aiogram 3.2.0**
- Telegram Bot API framework
- Async/await support
- Built-in FSM and middlewares

**APScheduler 3.9.1**
- Cron-based task scheduling
- Timezone support (Europe/Moscow)

**aiohttp 3.9.1**
- Async HTTP client for payment API calls
- Session pooling via `AsyncRequestSession`

**Pydantic 2.5.2**
- Data validation
- Database model definitions

**SQLite**
- Embedded database (via Python sqlite3)
- File-based storage at `tgbot/data/database.db`

## Utility Libraries

- **colorlog** - Colored console logging
- **beautifulsoup4** - HTML parsing/cleaning
- **aiofiles** - Async file operations
- **cachetools** - TTL cache for throttling
- **pytz** - Timezone handling