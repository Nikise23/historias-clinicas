import unittest
from unittest.mock import patch

from consultorio.storage import queries as q


class BuscarTurnosProximosTests(unittest.TestCase):
    @patch("consultorio.storage.queries.use_database", return_value=False)
    @patch("consultorio.storage.queries.cargar_json")
    def test_filtra_por_dni_y_fecha(self, mock_cargar, _db):
        def _store(path):
            if path.endswith("pacientes.json"):
                return [
                    {"dni": "37863139", "nombre": "Ana", "apellido": "Perez"},
                    {"dni": "11111111", "nombre": "Otro", "apellido": "Lopez"},
                ]
            if path.endswith("turnos.json"):
                return [
                    {
                        "dni_paciente": "37863139",
                        "fecha": "2026-09-10",
                        "hora": "10:00",
                        "medico": "Julieta Colom",
                        "estado": "sin atender",
                    },
                    {
                        "dni_paciente": "37863139",
                        "fecha": "2026-01-01",
                        "hora": "09:00",
                        "medico": "Julieta Colom",
                        "estado": "atendido",
                    },
                    {
                        "dni_paciente": "11111111",
                        "fecha": "2026-09-11",
                        "hora": "11:00",
                        "medico": "Francisco Colom",
                        "estado": "sin atender",
                    },
                ]
            return []

        mock_cargar.side_effect = _store
        res = q.buscar_turnos_proximos("37863139", "2026-09-10", limit=20)
        self.assertEqual(len(res), 1)
        self.assertEqual(res[0]["hora"], "10:00")

    @patch("consultorio.storage.queries.use_database", return_value=False)
    @patch("consultorio.storage.queries.cargar_json")
    def test_filtra_por_apellido(self, mock_cargar, _db):
        def _store(path):
            if path.endswith("pacientes.json"):
                return [{"dni": "37863139", "nombre": "Ana", "apellido": "Perez"}]
            if path.endswith("turnos.json"):
                return [
                    {
                        "dni_paciente": "37863139",
                        "fecha": "2026-09-12",
                        "hora": "10:00",
                        "medico": "Julieta Colom",
                    }
                ]
            return []

        mock_cargar.side_effect = _store
        res = q.buscar_turnos_proximos("pere", "2026-09-10", limit=20)
        self.assertEqual(len(res), 1)


if __name__ == "__main__":
    unittest.main()
