import pandas as pd
from sqlmodel import SQLModel, Session, Field
import uuid
from sqlalchemy import create_engine
from pathlib import Path


class PlayerCSVToDB(SQLModel):
    @staticmethod
    def create_csv(
        csv_name: str,
        headers: list
    ) -> None:
        """
        Create a .csv with the player's categories

        Args:
            csv_name: str: csv's name
            headers: list: header's columns
        """

        df = pd.DataFrame(columns=headers)

        df.to_csv(csv_name, index=False)


    def create_player(
        csv_name: str,
        data_player: list
    ):
        """
        Create a player in a csv.

        Args:
            df (pd.DataFrame): DataFrame where we want to save the player.
            player_data (dict): DICT with the player's data.
            csv_file_path (str): csv path.
        """
        df = pd.read_csv(csv_name)

        # Creamos un DataFrame con los datos del jugador
        new_player = pd.DataFrame([data_player], columns=df.columns)

        # Concatenamos el nuevo jugador con el DataFrame existente
        df = pd.concat([df, new_player], ignore_index=True)

        # Guardamos el DataFrame actualizado en el CSV
        df.to_csv(csv_name, index=False)

        """with open(csv_name, 'r') as archivo_csv:
            # Lee los datos del archivo CSV, excluyendo la primera fila (encabezados)
            datos_csv = archivo_csv.readlines()[1:]

            jugador = [
                player_id: uuid.UUID = Field(
                    default_factory=uuid.uuid4,
                    primary_key=True,
                    unique=True,
                    index=True,
                    sa_column_kwargs={"comment": "Unique identifier for the player"},
                ),
                'name': str(jugador_data[0]),
                'age': int(jugador_data[1]),
                'weight': int(jugador_data[2]),
                'height': float(jugador_data[3]),
                'salary': float(jugador_data[4]),
                'position': str(jugador_data[5]),
                'pac': float(jugador_data[6]),
                'sho': float(jugador_data[7]),
                'pas': float(jugador_data[8]),
                'dri': float(jugador_data[9]),
                'defe': float(jugador_data[10]),
                'phy': float(jugador_data[11]),
                'goalkeeping': float(jugador_data[12])]
            
            session.add(jugador)"""
