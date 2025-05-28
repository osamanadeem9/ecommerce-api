if __name__ == "__main__":
    print("Seeding database with dummy data...")

    from seed_data import seed_database

    seed_database()

    print("Database seeding completed!")
