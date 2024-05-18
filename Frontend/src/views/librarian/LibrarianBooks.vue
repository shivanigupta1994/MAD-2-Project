<template>
  <div class="container mt-3">

    <!-- Add Book Form -->
    <div class="card mt-4 mb-4" style="width: 50%;">
      <div class="card-header bg-primary text-white">
        Add Book
      </div>
      <div class="card-body">
        <form @submit.prevent="addBook">
          <div class="mb-3">
            <label for="bookName" class="form-label">Book Name</label>
            <input v-model="newBook.name" type="text" class="form-control" id="bookName" required>
          </div>
          <div class="mb-3">
            <label for="content" class="form-label">Content</label>
            <textarea v-model="newBook.content" class="form-control" id="content" rows="1" required></textarea>
          </div>
          <div class="row">
            <div class="col-md-6 mb-3">
              <label for="isbn" class="form-label">ISBN</label>
              <input v-model="newBook.isbn" type="text" class="form-control" id="isbn" required>
            </div>
            <div class="col-md-6 mb-3">
              <label for="author" class="form-label">Author</label>
              <input v-model="newBook.author" type="text" class="form-control" id="author" required>
            </div>
          </div>
          <div class="mb-3">
            <label for="number_of_pages" class="form-label">Number of Pages</label>
            <input v-model="newBook.number_of_pages" type="number" class="form-control" id="number_of_pages" required>
          </div>
          <div class="mb-3">
            <label for="image_url" class="form-label">Image</label>
            <input v-model="newBook.image_url" type="text" class="form-control" id="image_url" required>
          </div>
          <div class="mb-3">
            <label for="pdf_url" class="form-label">PDF</label>
            <input v-model="newBook.pdf_url" type="text" class="form-control" id="pdf_url" required>
          </div>
          <div class="mb-3">
            <label for="epub_url" class="form-label">EPUB</label>
            <input v-model="newBook.epub_url" type="text" class="form-control" id="epub_url" required>
          </div>
          <div class="mb-3">
            <label for="price" class="form-label">Price</label>
            <input v-model="newBook.price" type="number" class="form-control" id="price" required>
          </div>
          <div class="mb-3">
            <label for="sectionId" class="form-label">Section</label>
            <select v-model="newBook.section_id" class="form-control" id="sectionId" required>
              <option v-for="section in sections" :key="section.id" :value="section.id">{{ section.name }}</option>
            </select>
          </div>
          <button type="submit" class="btn btn-primary">Add Book</button>
        </form>
      </div>
    </div>

    <!-- Display Books -->
    <div class="card mt-4 mb-4" style="width: 100%; ">
      <div class="card-header bg-info text-white">
        All Books
      </div>
      <div class="card-body">
        <table class="table table-striped">
          <thead>
            <tr>
              <th>ID</th>
              <th>Name</th>
              <th>Content</th>
              <th>Pages</th>
              <th>ISBN</th>
              <th>Author</th>
              <th>Date Created</th>
              <th>Date Updated</th>
              <th>Image</th>
              <th>PDF</th>
              <th>EPUB</th>
              <th>Price</th>
              <th>Section ID</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="book in books" :key="book.id">
              <td>{{ book.id }}</td>
              <td>{{ book.name }}</td>
              <td>{{ book.content }}</td>
              <td>{{ book.number_of_pages }}</td>
              <td>{{ book.isbn }}</td>
              <td>{{ book.author }}</td>
              <td>{{ book.date_created }}</td>
              <td>{{ book.date_updated }}</td>
              <td>{{ book.image_url }}</td>
              <td>{{ book.pdf_url }}</td>
              <td>{{ book.epub_url }}</td>
              <td>{{ book.price }}</td>
              <td>{{ book.section_id }}</td>
              <td>
                <button @click="editBook(book)" class="btn btn-warning btn-sm m-1">Edit</button>
                <button @click="deleteBook(book.id)" class="btn btn-danger btn-sm m-1">Delete</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Edit Book Form -->
    <div v-if="editingBook" class="card mt-4 mb-4">
      <div class="card-header bg-success text-white">
        Edit Book
      </div>
      <div class="card-body">
        <form @submit.prevent="updateBook">
          <div class="mb-3">
            <label for="editBookName" class="form-label">Book Name</label>
            <input v-model="editingBook.name" type="text" class="form-control" id="editBookName" required>
          </div>
          <div class="mb-3">
            <label for="editContent" class="form-label">Content</label>
            <textarea v-model="editingBook.content" class="form-control" id="editContent" rows="1" required></textarea>
          </div>
          <div class="row">
            <div class="col-md-6 mb-3">
              <label for="editISBN" class="form-label">ISBN</label>
              <input v-model="editingBook.isbn" type="text" class="form-control" id="editISBN" required>
            </div>
            <div class="col-md-6 mb-3">
              <label for="editAuthor" class="form-label">Author</label>
              <input v-model="editingBook.author" type="text" class="form-control" id="editAuthor" required>
            </div>
          </div>
          <div class="mb-3">
            <label for="editnumber_of_pages" class="form-label">Number of Pages</label>
            <input v-model="editingBook.number_of_pages" type="number" class="form-control" id="number_of_pages" required>
          </div>
          <div class="mb-3">
            <label for="editimage_url" class="form-label">Image</label>
            <input v-model="editingBook.image_url" type="text" class="form-control" id="image_url" required>
          </div>
          <div class="mb-3">
            <label for="editpdf_url" class="form-label">PDF</label>
            <input v-model="editingBook.pdf_url" type="text" class="form-control" id="image_url" required>
          </div>
          <div class="mb-3">
            <label for="editepub_url" class="form-label">EPUB</label>
            <input v-model="editingBook.epub_url" type="text" class="form-control" id="epub_url" required>
          </div>
          <div class="mb-3">
            <label for="editprice" class="form-label">Price</label>
            <input v-model="editingBook.price" type="number" class="form-control" id="price" required>
          </div>
          <div class="mb-3">
            <label for="editSectionId" class="form-label">Section</label>
            <select v-model="editingBook.section_id" class="form-control" id="editSectionId" required>
              <option v-for="section in sections" :key="section.id" :value="section.id">{{ section.name }}</option>
            </select>
          </div>
          <button type="submit" class="btn btn-success">Update Book</button>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      newBook: {
        name: '',
        content: '',
        isbn: '',
        author: '',
        section_id: '',
        number_of_pages: '',
        image_url: '',
        pdf_url: '',
        epub_url: ''
      },
      books: [],
      editingBook: null,
      sections: []
    };
  },
  mounted() {
    this.getAllBooks();
    this.getAllSections();
  },
  methods: {
    async addBook() {
      try {
        const response = await this.$axios.post('/book', this.newBook);
        this.getAllBooks();
        // Clear the form after adding the book
        this.newBook = {
          name: '',
          content: '',
          isbn: '',
          author: '',
          section_id: '',
          number_of_pages: '',
          image_url: '',
          pdf_url: '',
          epub_url: ''
        };
      } catch (error) {
        console.error('Add Book failed:', error);
      }
    },
    async getAllBooks() {
      try {
        const response = await this.$axios.get('/book');
        this.books = response.data;
      } catch (error) {
        console.error('Get Books failed:', error);
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
    editBook(book) {
      this.editingBook = { ...book };
    },
    async updateBook() {
      try {
        await this.$axios.put(`/book`, {
          id: this.editingBook.id,
          name: this.editingBook.name,
          content: this.editingBook.content,
          isbn: this.editingBook.isbn,
          author: this.editingBook.author,
          section_id: this.editingBook.section_id,
          number_of_pages: this.editingBook.number_of_pages,
          image_url: this.editingBook.image_url,
          pdf_url: this.editingBook.pdf_url,
          epub_url: this.editingBook.epub_url
        }).then(() => {
          // alert response message
          alert(this.editingBook.name + ' updated successfully !!')
        });

        this.editingBook = null;
        this.getAllBooks();
      } catch (error) {
        console.error('Update Book failed:', error);
      }
    },
    async deleteBook(bookId) {
      try {
        await this.$axios.delete(`/book`, { data: { id: bookId } });
        this.getAllBooks();
      } catch (error) {
        console.error('Delete Book failed:', error);
      }
    }
  }
};
</script>

<style scoped>
.table tbody tr td {
  /* white-space: nowrap; */
  overflow: hidden;
  text-overflow: clip;
}

.table tbody tr td:last-child {
  white-space: nowrap;
}

/* Center the card in the middle of the page */
.container {
  display: flex;
  justify-content: center;
  align-items: left;
  min-height: 90vh;
  overflow: auto;
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
  /* max-height: 500px; */
  overflow-y: auto;
}

/* Custom styles for the form headers */
.card-header.bg-primary,
.card-header.bg-info,
.card-header.bg-success {
  text-align: center;
  font-size: 1.2rem;
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

/* Hover effect for table rows */
.table-hover tbody tr:hover {
  background-color: #e2e6ea;
}
</style>
