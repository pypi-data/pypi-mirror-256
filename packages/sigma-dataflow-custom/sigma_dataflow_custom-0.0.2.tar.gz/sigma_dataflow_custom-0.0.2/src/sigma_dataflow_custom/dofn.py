import apache_beam as beam
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)

class FormatDoFn(beam.DoFn):
    def process(self, row, schema):
        """Retorna un diccionaro con keys segun el schema 
        y values con elementos de row.

        Args:
            row (_type_): lista con elementos por filas
            schema (_type_): diccionario con el schema de la tabla en bigquery

        Returns:
            list[dict]: se torna una lista (x cuestiones de apache beam) con el diccionario
        """
        # Column names or headers.
        fields_names = [field["name"] for field in schema["fields"]]
        
        # Column data type: INT64, NUMERIC, STRING, DATETIME, etc.
        fields_type = [field["type"] for field in schema["fields"]]
        
        # Column mode: NULLABLE, REQUIRED.
        fields_mode = [field["mode"] for field in schema["fields"]]
        
        # La lista de elementos (row) la convertimos en un diccionario donde cada key es el nombre de su columna correspondient en la tabla output.
        errors = []
        output = {}
        # Filtra los elementos a su vez, ya que unicamente recorre las columnas del schema.
        for i in range(len(fields_names)):
            element = row[i]
            
            try:
                if fields_mode[i] == "REQUIRED" and element is None:
                    logging.error(f"Elemento = {element} es None cuando el campo es {fields_mode[i]}")
                    errors.append(element)
                    continue
            except Exception as e:
                logging.error(f"Elemento = {element} genero el error: {str(e)}")
                errors.append(element)
                continue
            
            try:
                if fields_type[i] == "INT64" or fields_type[i] == "INTEGER":
                    element = int(element)
                elif fields_type[i] == "NUMERIC":
                    element = float(element)
                elif fields_type[i] == "DATE":
                    element = datetime.strptime(element, "%Y-%m-%d").date()
                elif fields_type[i] == "DATETIME":
                    element = datetime.strptime(element, "%Y-%m-%d %H:%M:%S")
                else:
                    element = str(element)
            except Exception as e:
                logging.error(f"Elemento = {element} genero el error: {str(e)}")
                errors.append(element)
                continue
            output[fields_names[i]] = element
        return [output]