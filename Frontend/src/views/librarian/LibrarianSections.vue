<template>
  <div class="container ">

    <!-- Add Section Form -->
    <div class="card mt-4 addsec">
      <div class="card-header bg-primary text-white">
        Add Section
      </div>
      <div class="card-body">
        <form @submit.prevent="addSection">
          <div class="mb-3">
            <label for="sectionName" class="form-label">Section Name</label>
            <input v-model="newSection.name" type="text" class="form-control" id="sectionName" required>
          </div>
          <div class="mb-3">
            <label for="description" class="form-label">Description</label>
            <textarea v-model="newSection.description" class="form-control" id="description" rows="1" required></textarea>
          </div>
          <button type="submit" class="btn btn-primary">Add Section</button>
        </form>
      </div>
    </div>

    <!-- Display Sections -->
    <div class="card mt-4 dissec ">
      <div class="card-header bg-info text-white">
        All Sections
      </div>
      <div class="">
        <table class="table table-striped ">
          <thead>
            <tr>
              <th>ID</th>
              <th>Name</th>
              <th>Description</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="section in sections" :key="section.id">
              <td>{{ section.id }}</td>
              <td>{{ section.name }}</td>
              <td>{{ section.description }}</td>
              <td>
                <button @click="editSection(section)" class="btn btn-warning btn-sm m-1">Edit</button>
                <button @click="deleteSection(section.id)" class="btn btn-danger btn-sm m-1">Delete</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Edit Section Form -->
    <div v-if="editingSection" class="card mt-4 mb-4 esf">
      <div class="card-header bg-success text-white">
        Edit Section
      </div>
      <div class="card-body">
        <form @submit.prevent="updateSection">
          <div class="mb-3">
            <label for="editSectionName" class="form-label">Section Name</label>
            <input v-model="editingSection.name" type="text" class="form-control" id="editSectionName" required>
          </div>
          <div class="mb-3">
            <label for="editDescription" class="form-label">Description</label>
            <textarea v-model="editingSection.description" class="form-control" id="editDescription" rows="1"
              required></textarea>
          </div>
          <button type="submit" class="btn btn-success">Update Section</button>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      newSection: {
        name: '',
        description: ''
      },
      sections: [],
      editingSection: null
    };
  },
  mounted() {
    this.getAllSections();
  },
  methods: {
    async addSection() {
      try {
        const response = await this.$axios.post('/section', this.newSection);
        this.getAllSections();
        // Clear the form after adding the section
        this.newSection = {
          name: '',
          description: ''
        };
      } catch (error) {
        console.error('Add Section failed:', error);
      }
    },
    async getAllSections() {
      try {
        const response = await this.$axios.get('/section');
        this.sections = response.data;
      } catch (error) {
        console.error('Get Sections failed:', error);
      }
    },
    editSection(section) {
      this.editingSection = { ...section };
    },
    async updateSection() {
      try {
        await this.$axios.put(`/section`, {
          id: this.editingSection.id,
          name: this.editingSection.name,
          description: this.editingSection.description
        }).then(() => {
          // alert response message
          alert(this.editingSection.name + ' updated successfully !!')
        });

        this.editingSection = null;
        this.getAllSections();
      } catch (error) {
        console.error('Update Section failed:', error);
      }
    },
    async deleteSection(sectionId) {
      try {
        await this.$axios.delete(`/section`, { data: { id: sectionId } });
        this.getAllSections();
      } catch (error) {
        console.error('Delete Section failed:', error);
      }
    }

  }
};
</script>

<style scoped>
.table tbody tr td {
  /* white-space: nowrap; */
  overflow: hidden;
  text-overflow: ellipsis;
}

.table tbody tr td:last-child {
  white-space: nowrap;
}

.addsec {
  width: 50%;
  /* margin: auto; */
  margin-left: 10px;

}


.esf {
  width: 50%;

}

/* Center the card in the middle of the page */
.container {
  display: flex;
  margin-left: 120px;
  width: 120%;


}

/* Add some spacing to the buttons for better readability */
.btn {
  margin-right: 5px;
}

/* Make the card header text bold */
.card-header {
  font-weight: bold;
}

.card-body {
  max-height: 100vh;

  overflow-y: auto;
}

/* Custom styles for the form headers */
.card-header.bg-primary,
.card-header.bg-info,
.card-header.bg-success {
  /* text-align: center; */
  font-size: 1.2rem;
}

/* Add some spacing to the top of the table */
.table {
  margin-top: 15px;
}

/* Style table header */
.table thead th {
  background-color: #343a40;
  color: white;
}

/* Style alternating rows in the table */
.table-striped tbody tr:nth-child(odd) {
  background-color: #f8f9fa;
}
</style>
