import DobotDllType as dType
import time

# Cargar la API de Dobot
api = dType.load()

# Configurar el puerto COM del Dobot
PORT = "COM3"  # Cambie "COM3" por el puerto correcto
state = dType.ConnectDobot(api, PORT, 115200)

# Verificar si la conexión fue exitosa
if state[0] != dType.DobotConnect.DobotConnect_NoError:
    print("Error al conectar con Dobot")
    exit()
else:
    print("Conexión exitosa al Dobot")

# Configurar el puerto del sensor como entrada digital
input_port = 15  # Dirección del puerto de entrada digital
dType.SetIOMultiplexing(api, input_port, 3)  # 0 indica entrada digital

# Configuracion de los puertos para los leds verde y azul
dType.SetIOMultiplexing(api, 6, 1) # Led azul
dType.SetIOMultiplexing(api, 4, 1) # Led verde 

# Configurar el comando de tiempo de espera y la cola de comandos
dType.SetCmdTimeout(api, 10000)
dType.SetQueuedCmdClear(api)  # Limpiar cualquier comando anterior

# Inicializar el Dobot
dType.SetQueuedCmdStartExec(api)  # Iniciar la ejecución de la cola

# Función para obtener las coordenadas actuales
def get_current_position():
    # Obtener la posición actual (X, Y, Z, Angulo de herramienta)
    pose = dType.GetPose(api)
    return pose[0], pose[1], pose[2]  # X, Y, Z

# Esperar un poco para que el robot inicie completamente
time.sleep(2)

dType.SetIODO(api, 6, False) # Se apagan ambos leds al inciar el programa
dType.SetIODO(api, 4, False) # Se apagan ambos leds al inciar el programa

# Ir a posición inicial con Home
dType.SetHOMECmd(api, 0)
time.sleep(22)  # Esperar a que termine el movimiento

# Cerrar el gripper
dType.SetEndEffectorGripper(api, 1, 1)  # Activar el gripper (cerrar)
print("Gripper cerrado")
time.sleep(2)
dType.SetEndEffectorSuctionCup(api, 0, 0)  # Apagar completamente la bomba de aire
time.sleep(2)

# Posicion Inicial Elevada
dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, 299, 24, 120, 100)
time.sleep(3)

# Condicional para leer la entrada del sensor
try:
    while True:
        # Leer el estado del puerto como entrada digital
        sensor_value = dType.GetIODI(api, input_port)  # Devuelve 0 (bajo) o 1 (alto)
        # Verificar si la lectura fue exitosa
        if sensor_value != -1:
            print(f"Sensor Value: {sensor_value}")
            time.sleep(3)
            if sensor_value == [0]: 
                dType.SetIODO(api, 4, False)
                print("Se detecto un cubito")

                # Encima de la caja para recogerla
                dType.SetIODO(api, 6, True) # Se enciende led Azul
                dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, 90, 210, 25, 10)

                # Comprobar la posición antes de abrir el gripper
                time.sleep(6)
                print(get_current_position())
                current_x, current_y, current_z = get_current_position()

                # Condicional if para abrir el gripper solo si está en la posición deseada
                if current_x == 90.0 and current_y == 209.99998474121094 and current_z == 25.0:
                # Abrir el gripper si el robot está en las coordenadas correctas
                    dType.SetEndEffectorGripper(api, 1, 0)  # Desactivar el gripper (abrir)
                    print("Gripper abierto")
                    time.sleep(2)
                else: 
                    print("Error gripper no se abrio")

                # Recogiendo la caja 
                dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, 90, 210, -17, 10)
                time.sleep(2)

                # Cerrar el gripper
                dType.SetEndEffectorGripper(api, 1, 1)  # Activar el gripper (cerrar)
                print("Gripper cerrado")
                time.sleep(2)
                dType.SetEndEffectorSuctionCup(api, 0, 0)  # Apagar completamente la bomba de aire
                time.sleep(2)

                # Posicion Inicial Elevada
                dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, 299, 24, 120, 100)
                time.sleep(3)

                # En posición encima de la base para dejar la caja
                dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, 50, -290, 50, 15)
                time.sleep(2)

                # En posición para dejar la caja
                dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, 50, -290, -17, 15)
                time.sleep(2)

                # Comprobar la posición antes de abrir el gripper
                time.sleep(6)
                print(get_current_position())
                current_x, current_y, current_z = get_current_position()
                # Condicional if para abrir el gripper solo si está en la posición deseada
                if current_x == 49.9999885559082 and current_y == -289.9999694824219 and current_z == -17.0:
                    # Abrir el gripper si el robot está en las coordenadas correctas
                    dType.SetEndEffectorGripper(api, 1, 0)  # Desactivar el gripper (abrir)
                    print("Gripper abierto")
                    time.sleep(2)

                # En posición encima de la base para dejar la caja
                dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, 50, -290, 50, 15)

                # Cerrar el gripper
                time.sleep(6)
                dType.SetEndEffectorGripper(api, 1, 1)  # Activar el gripper (cerrar)
                print("Gripper cerrado")
                time.sleep(2)
                dType.SetEndEffectorSuctionCup(api, 0, 0)  # Apagar completamente la bomba de aire
                time.sleep(2)

                # Posicion Inicial Elevada
                dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, 299, 24, 120, 100)
                time.sleep(3)

                dType.SetIODO(api, 6, False) # Se apaga Led azul
                print(dType.GetIODO(api, 6))

            else: 
             if sensor_value == [1]:
                print("No se detecto nada")
                dType.SetIODO(api, 4, True)

        else:
            print("Error al leer el valor del puerto.")

        time.sleep(0.1)  # Pausa para evitar sobrecargar el procesador

except KeyboardInterrupt:
    print("Programa detenido.")

    dType.SetIODO(api, 6, False) # Se apagan ambos leds al inciar el programa
    dType.SetIODO(api, 4, False) # Se apagan ambos leds al inciar el programa

    # Desactivar la bomba de aire comprimido al finalizar
    dType.SetEndEffectorSuctionCup(api, 0, 0)  # Apagar completamente la bomba de aire
    print("Bomba de aire comprimido desactivada.")
    print("Movimientos finalizados")

finally:
    # Finalizar conexión
    dType.DisconnectDobot(api)
    print("Conexión cerrada.")