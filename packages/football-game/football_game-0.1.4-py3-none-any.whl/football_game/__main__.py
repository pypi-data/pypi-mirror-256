import csv
from decouple import config
from sqlmodel import create_engine, SQLModel, Session
from sqlmodel import Session

from schemas import *


def main():
    postgres_uri: str = config("POSTGRES_URI")
    engine = create_engine(postgres_uri)
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        
        csv_name = "football_game/schemas/test_player.csv"

        headers = ["name",
            "age",
            "weight",
            "height",
            "salary",
            "position",
            "pac",
            "sho",
            "pas",
            "dri",
            "defe",
            "phy",
            "goalkeeping"]
        
        PlayerCSVToDB.create_csv(
            csv_name, 
            headers,
        )

        player_data = [
            "Carlos",
            25,
            70,
            1.75,
            100000,
            "Forward",
            85,
            90,
            80,
            85,
            40,
            75,
            0
        ]
        PlayerCSVToDB.create_player(
            csv_name,
            player_data
        )

        session.add()
        session.commit()
        print("Data inserted successfully!")


if __name__ == "__main__":
    main()