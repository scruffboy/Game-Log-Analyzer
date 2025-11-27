# Game Logs Analysis System

## 📋 Project Overview

A high-performance system for processing and analyzing game server logs with real-time statistics and interactive querying capabilities.

## 👨‍💻 Author

**Zakhvatkin Kirill Evgenievich**  
_Python Developer_  
**Completion Date:** 25.11.2024

## 🏗 Project Structure

Parse_logs/
├── src/
│ ├── logs/ # Log files directory
│ │ ├── inventory_logs.txt # Input: item transactions
│ │ ├── money_logs.txt # Input: money operations
│ │ ├── combined_log.txt # Output: merged sorted logs
│ │ └── output.txt # Output: analytics results
│ └── modules/
│ │ └── generate_sample_logs.py # Test data generator
├── main.py # Main application
└── README.md

## 🚀 Features

- **Multi-format Log Parsing** - handles different log structures
- **Large-scale Data Processing** - optimized for 10M+ records
- **Real-time Statistics** - player rankings, item analytics
- **Interactive CLI** - live item search across players
- **Data Generation** - sample log generator for testing

## 🛠 Tech Stack

- Python 2.7.18 - 3+ (standard libraries only)
- Object-Oriented Architecture
- Memory-efficient stream processing
- Custom sorting algorithms
