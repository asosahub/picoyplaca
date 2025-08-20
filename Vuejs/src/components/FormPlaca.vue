<template>
    <div>
        <h2>Verificar Pico y Placa</h2>
        <form @submit.prevent="enviarFormulario">
            <div>
                <label for="placa">Ingrese la placa de su vehiculo:</label>
                <input type="text" id="placa" v-model="placa" required/>
            </div>
            <button type="submit">Verificar</button>
        </form>
    </div>
</template>

<script>
export default {
    name: "FormPlaca",
    data() {
        return {
            placa: "",
        }
    },
    methods: {
        enviarFormulario() {
            //no hace nada
        }
    }
};
</script>

<style scoped>
.form-container {
  max-width: 350px;
  margin: 60px auto;
  background: #fff;
  padding: 32px 24px;
  border-radius: 12px;
  box-shadow: 0 6px 24px rgba(80, 80, 80, 0.12);
  text-align: center;
  font-family: 'Segoe UI', 'Arial', sans-serif;
}

h2 {
  margin-bottom: 28px;
  color: #42b983;
  font-weight: 600;
  font-size: 1.3rem;
}

.form-group {
  margin-bottom: 20px;
  text-align: left;
}

label {
  display: block;
  margin-bottom: 7px;
  color: #555;
  font-size: 1rem;
}

input[type="text"] {
  width: 100%;
  padding: 10px;
  border: 1px solid #d6d6d6;
  border-radius: 6px;
  font-size: 1rem;
  transition: border-color 0.2s;
  box-sizing: border-box;
}

input[type="text"]:focus {
  border-color: #42b983;
  outline: none;
}

button {
  padding: 10px 24px;
  background: #42b983;
  color: #fff;
  border: none;
  border-radius: 6px;
  font-size: 1rem;
  font-weight: 500;
  cursor: pointer;
  transition: background 0.2s;
  margin-top: 8px;
}

button:hover {
  background: #369870;
}
</style>