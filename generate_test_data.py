#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
JMeter Test Data Generator
Generate random test data for Alipay payment stress testing

Generate random data:
- order_id: Order ID (format: ORDER + timestamp + random string)
- password: Payment password (simulate real scenarios, include correct and wrong passwords)
- amount: Payment amount (random amount range)
"""

import csv
import random
import time
import string
import argparse
from datetime import datetime


class TestDataGenerator:
    """Test data generator class"""
    
    def __init__(self):
        # Password pool (include correct password 123456 and common wrong passwords)
        self.password_pool = [
            '123456',  # Correct password
            '123456',  # Increase correct password weight
            '123456',  # Increase correct password weight
            '111111',  # Common wrong password
            '000000',  # Common wrong password
            '888888',  # Common wrong password
            '666666',  # Common wrong password
            '123123',  # Common wrong password
            'password',  # Common wrong password
            '1234',     # Short password
            '12345678', # Long password
        ]
        
        # Amount ranges (simulate real payment scenarios)
        self.amount_ranges = [
            (10.00, 50.00),      # Small amount
            (50.00, 200.00),     # Medium amount
            (200.00, 500.00),    # Large amount
            (500.00, 1000.00),   # High amount
            (1000.00, 5000.00),  # Very high amount
        ]
        
        # Amount weights (small amounts are more common)
        self.amount_weights = [0.4, 0.3, 0.2, 0.08, 0.02]
    
    def generate_order_id(self, index=None):
        """
        Generate order ID
        Format: ORDER + timestamp + random string
        """
        timestamp = int(time.time() * 1000)  # Millisecond timestamp
        random_suffix = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        
        if index is not None:
            return f"ORDER{index:06d}{random_suffix}"
        else:
            return f"ORDER{timestamp}{random_suffix}"
    
    def generate_password(self):
        """
        Generate payment password
        Randomly select password based on weights (correct password has higher weight)
        """
        return random.choice(self.password_pool)
    
    def generate_amount(self):
        """
        Generate payment amount
        Randomly select amount range based on weights, then generate random amount within range
        """
        # Select amount range based on weights
        amount_range = random.choices(self.amount_ranges, weights=self.amount_weights)[0]
        
        # Generate random amount within selected range
        min_amount, max_amount = amount_range
        amount = round(random.uniform(min_amount, max_amount), 2)
        
        return amount
    
    def generate_test_data(self, num_records=1000):
        """
        Generate specified number of test data records
        
        Args:
            num_records (int): Number of records to generate
            
        Returns:
            list: List containing test data
        """
        test_data = []
        
        print(f"Generating {num_records} test data records...")
        
        for i in range(num_records):
            order_id = self.generate_order_id(i + 1)
            password = self.generate_password()
            amount = self.generate_amount()
            
            test_data.append({
                'order_id': order_id,
                'password': password,
                'amount': amount
            })
            
            # Show progress
            if (i + 1) % 100 == 0:
                print(f"Generated {i + 1} records...")
        
        print(f"Test data generation completed! Generated {len(test_data)} records")
        return test_data
    
    def save_to_csv(self, test_data, filename='JMeter_test_data.csv'):
        """
        Save test data to CSV file
        
        Args:
            test_data (list): List of test data
            filename (str): Output filename
        """
        try:
            with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                fieldnames = ['order_id', 'password', 'amount']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                
                # Write header
                writer.writeheader()
                
                # Write data
                writer.writerows(test_data)
            
            print(f"Test data saved to file: {filename}")
            
            # Show statistics
            self.show_statistics(test_data)
            
        except Exception as e:
            print(f"Error saving file: {e}")
    
    def show_statistics(self, test_data):
        """
        Show test data statistics
        
        Args:
            test_data (list): List of test data
        """
        print("\n=== Test Data Statistics ===")
        print(f"Total records: {len(test_data)}")
        
        # Password statistics
        password_counts = {}
        for record in test_data:
            password = record['password']
            password_counts[password] = password_counts.get(password, 0) + 1
        
        print("\nPassword distribution:")
        for password, count in sorted(password_counts.items(), key=lambda x: x[1], reverse=True):
            percentage = (count / len(test_data)) * 100
            print(f"  {password}: {count} times ({percentage:.1f}%)")
        
        # Amount statistics
        amounts = [record['amount'] for record in test_data]
        print(f"\nAmount statistics:")
        print(f"  Min amount: ¥{min(amounts):.2f}")
        print(f"  Max amount: ¥{max(amounts):.2f}")
        print(f"  Average amount: ¥{sum(amounts)/len(amounts):.2f}")
        
        # Amount range statistics
        ranges = [
            (0, 50, "Small (0-50)"),
            (50, 200, "Medium (50-200)"),
            (200, 500, "Large (200-500)"),
            (500, 1000, "High (500-1000)"),
            (1000, float('inf'), "Very High (1000+)")
        ]
        
        print("\nAmount range distribution:")
        for min_val, max_val, label in ranges:
            count = sum(1 for amount in amounts if min_val <= amount < max_val)
            percentage = (count / len(amounts)) * 100
            print(f"  {label}: {count} times ({percentage:.1f}%)")


def main():
    """Main function"""
    parser = argparse.ArgumentParser(description='JMeter Test Data Generator')
    parser.add_argument('-n', '--num-records', type=int, default=1000,
                       help='Number of test records to generate (default: 1000)')
    parser.add_argument('-o', '--output', type=str, default='JMeter_test_data.csv',
                       help='Output filename (default: JMeter_test_data.csv)')
    parser.add_argument('--seed', type=int, default=None,
                       help='Random seed for generating reproducible test data')
    
    args = parser.parse_args()
    
    # Set random seed (if provided)
    if args.seed is not None:
        random.seed(args.seed)
        print(f"Using random seed: {args.seed}")
    
    # Create generator instance
    generator = TestDataGenerator()
    
    # Generate test data
    test_data = generator.generate_test_data(args.num_records)
    
    # Save to CSV file
    generator.save_to_csv(test_data, args.output)
    
    print(f"\nTest data generation completed!")
    print(f"File location: {args.output}")
    print(f"Record count: {len(test_data)}")
    print(f"Generation time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")


if __name__ == '__main__':
    main()
