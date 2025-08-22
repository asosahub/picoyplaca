<template>
  <div class="container-fluid vh-100 d-flex align-items-center justify-content-center">
    <form @submit.prevent="sendForm" class="bg-white p-4 rounded shadow" style="min-width: 340px;">
      <h2>Verificar Pico y Placa</h2>
      <div class="form-floating mb-3">
        <input
          type="text"
          class="form-control"
          id="license_plate"
          placeholder="ABC123"
          v-model="license_plate"
          maxlength="6"
          autocomplete="off"
          :disabled="loading"
          required
        >
        <label for="license_plate">Ingrese la placa de su vehiculo</label>
      </div>
      <button class="btn btn-success w-100" type="submit" :disabled="loading">
        {{ loading ? 'Verificando...' : 'Verificar' }}
      </button>
    </form>

    <div v-if="showModal" class="modal fade show d-block" tabindex="-1" style="background: rgba(0,0,0,0.4);">
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content">
          <div class="modal-header" :class="getHeaderClass()">
            <h5 class="modal-title">
              {{ getTitleText() }}
            </h5>
            <button type="button" class="btn-close btn-close-white" @click="closeModal"></button>
          </div>
          <div class="modal-body">
            <!-- Si hay error o el formato inválido -->
            <div v-if="error || (result && !result['valid_format'])" class="text-center">
              <i class="fas fa-exclamation-triangle text-danger fa-3x mb-3"></i>
              <p class="text-danger"><strong>{{ getErrorMessage() }}</strong></p>
              <div v-if="result && !result['valid_format']" class="mt-3 p-3 bg-light rounded">
                <small class="text-muted">
                  <strong>Formato correcto:</strong> 3 letras seguidas de 3 números<br>
                  <strong>Ejemplo:</strong> ABC123, XYZ789
                </small>
              </div>
            </div>

            <!-- Si hay resultado exitoso con formato válido -->
            <div v-else-if="result && result['valid_format']" class="text-center">
              <!-- Icono según el estado -->
              <i v-if="result['circulation_status']" class="fas fa-check-circle text-success fa-3x mb-3"></i>
              <i v-else class="fas fa-times-circle text-danger fa-3x mb-3"></i>

              <!-- Información de la consulta -->
              <div class="info-section mb-3">
                <p><strong>Fecha de hoy:</strong> {{ today }}</p>
                <p><strong>Placa:</strong> {{ result.license_plate }}</p>
                <p><strong>Último dígito:</strong> {{ result['last_digit'] }}</p>
              </div>

              <!-- Estado de circulación -->
              <div class="estado-section p-3 rounded" :class="result['circulation_status'] ? 'bg-light-success' : 'bg-light-danger'">
                <h6 class="mb-2" :class="result['circulation_status'] ? 'text-success' : 'text-danger'">
                  <strong>Estado de Circulación</strong>
                </h6>
                <p class="mb-0" :class="result['circulation_status'] ? 'text-success' : 'text-danger'">
                  <strong>
                    {{ result['circulation_status'] ? 'PUEDE CIRCULAR' : 'TIENE PICO Y PLACA' }}
                  </strong>
                </p>
                <small class="text-muted">{{ result.message }}</small>
              </div>

              <div class="mt-3">
                <div v-if="result['holiday']" class="p-2 bg-warning bg-opacity-25 rounded mb-2">
                  <small class="text-warning"><strong> Hoy es día festivo</strong></small>
                </div>
                <div v-if="!result['rush_hour']" class="p-2 bg-info bg-opacity-25 rounded mb-2">
                  <small class="text-info"><strong>Fuera del horario de pico y placa (6am - 9pm)</strong></small>
                </div>
                <div v-if="result['weekend']" class="p-2 bg-secondary bg-opacity-25 rounded">
                  <small class="text-secondary"><strong>Es fin de semana - No aplica pico y placa</strong></small>
                </div>
              </div>
            </div>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" @click="closeModal">Cerrar</button>
            <button type="button" class="btn btn-primary" @click="newConsult">Nueva Consulta</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: "FormPlaca",
  data() {
    return {
      license_plate: "",
      showModal: false,
      loading: false,
      result: null,
      error: null,
      today: ""
    }
  },
  mounted() {
    this.getToday();
  },
  methods: {
    getToday() {
      const now = new Date();
      this.today = now.toLocaleDateString('es-CO', {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        weekday: 'long'
      });
    },

    async sendForm() {
      if (!this.license_plate.trim()) {
        this.error = 'Por favor ingrese una placa válida';
        this.result = null;
        this.closeModal = true;
        return;
      }

      this.loading = true;
      this.error = null;
      this.result = null;

      try {
        const response = await axios.get('http://localhost:8000/api/validator-placa/', {
          params: {
            license_plate: this.license_plate.trim()
          }
        });
        
        this.result = response.data;
        this.showModal = true;
        
      } catch (err) {
        if (err.response && err.response.status === 400) {
          // Error de formato inválido
          this.result = err.response.data;
          this.error = null;
        } else {
          // Error de conexión u otro
          this.error = err.response?.data?.error || 'Error al conectar con el servidor. Verifique que el backend esté ejecutándose.';
          this.result = null;
        }
        console.error('Error:', err);
        this.showModal = true;
      } finally {
        this.loading = false;
      }
    },

    getHeaderClass() {
      if (this.error || (this.result && !this.result['valid_format'])) {
        return 'bg-danger text-white';
      }
      return this.result && this.result['circulation_status'] ? 'bg-success text-white' : 'bg-danger text-white';
    },

    getTitleText() {
      if (this.error || (this.result && !this.result['valid_format'])) {
        return 'Formato Inválido';
      }
      return 'Resultado de Verificación';
    },

    getErrorMessage() {
      if (this.error) {
        return this.error;
      }
      if (this.result && !this.result['valid_format']) {
        return this.result.message;
      }
      return 'Error desconocido';
    },

    closeModal() {
      this.showModal = false;
    },

    newConsult() {
      this.showModal = false;
      this.license_plate = "";
      this.result = null;
      this.error = null;
    }
  }
};
</script>

<style scoped>
h2 {
  margin-bottom: 28px;
  color: #42b983;
  font-weight: 600;
  font-size: 1.3rem;
}
</style>