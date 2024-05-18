<template>
  <div>

    <!-- Book Requests Table -->
    <div v-if="filteredBookRequests.length > 0" class="text-center">
      <h3 class="section-title">Book Requests</h3>
      <table class="table table-bordered table-striped">
        <thead>
          <tr>
            <th>ID</th>
            <th>Book Name</th>
            <th>Request Date</th>
            <th>Status</th>
            <th>Action</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="request in filteredBookRequests" :key="request.id">
            <td>{{ request.id }}</td>
            <td>{{ request.book_name }}</td>
            <td>{{ request.request_date }}</td>
            <td>{{ request.status }}</td>
            <td>
              <button class="btn btn-warning" v-if="request.status === 'Pending'"
                @click="deleteRequest(request.id)">Cancel</button>
              <button class="btn btn-secondary" v-if="request.status === 'Rejected'"
                @click="deleteRequest(request.id)">Delete</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
    <div v-else class="text-center">
      <hr>
      <h1>No book requests available.</h1>
    </div>

    <!-- Issued Books Table -->
    <div v-if="filteredIssuedBooks.length > 0" class="text-center">
      <h3 class="section-title">Issued Books</h3>
      <table class="table table-bordered table-striped">
        <thead>
          <tr>
            <th>ID</th>
            <th>Book Name</th>
            <th>Status</th>
            <th>Issue Date</th>
            <th>Rating</th>
            <th>Action</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="accessLog in filteredIssuedBooks" :key="accessLog.id">
            <td>{{ accessLog.id }}</td>
            <td>{{ accessLog.book_name }}</td>
            <td>{{ accessLog.status }}</td>
            <td>{{ accessLog.issue_date }}</td>
            <td>
              <!-- <select class="rating-select" v-model="accessLog.rating" v-if="accessLog.status === 'Issued'"> -->
              <div class="d-flex justify-content-center">
                <div class="col col-auto">
                  <select class="rating-select mr-2" v-model="accessLog.rating" v-if="accessLog.status === 'Issued'">
                    <option value="1">1</option>
                    <option value="2">2</option>
                    <option value="3">3</option>
                    <option value="4">4</option>
                    <option value="5">5</option>
                  </select>
                </div>
                <div class="col-7">
                  <button class="btn btn-primary submit-rating-btn" v-if="accessLog.status === 'Issued'"
                    @click="submitRating(accessLog)">Submit Rating</button>
                </div>
              </div>
            </td>
            <td>
              <button class="btn btn-danger m-1" v-if="accessLog.status === 'Issued'"
                @click="returnBook(accessLog.id)">Return</button>
              <button class="btn btn-danger" v-if="accessLog.status === 'Issued'"
                @click="pdf(accessLog.book_id, accessLog.price)">Download
                PDF for ₹{{ accessLog.price }}</button>
              <button class="btn btn-danger m-1" v-if="accessLog.status === 'Issued'"
                @click="read(accessLog.book_id)">Read</button>
              <span v-else-if="accessLog.status === 'Returned'" class="returned-date">Returned on {{
      accessLog.return_date
    }}</span>
              <span v-else-if="accessLog.status === 'Revoked'" class="revoked-date">Revoked on {{ accessLog.revoke_date
                }}</span>
              <span v-else>{{ accessLog.status }}</span>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
    <div v-else class="text-center">
      <hr>
      <h1>No issued books available.</h1>
    </div>
  </div>
</template>



<script>
export default {
  data() {
    return {
      bookRequests: [],
      issuedBooks: [],
    };
  },
  computed: {
    filteredBookRequests() {
      const user_id = localStorage.getItem('user_id');
      return this.bookRequests.filter(request => request.user_id === parseInt(user_id));
    },
    filteredIssuedBooks() {
      const user_id = localStorage.getItem('user_id');
      return this.issuedBooks.filter(accessLog => accessLog.user_id === parseInt(user_id));
    },
  },
  mounted() {
    this.fetchBookRequests();
    this.fetchIssuedBooks();
  },
  methods: {
    fetchBookRequests() {
      this.$axios.get('/book/request')
        .then(response => {
          this.bookRequests = response.data;
        })
        .catch(error => {
          console.error('Error fetching book requests', error);
        });
    },
    fetchIssuedBooks() {
      this.$axios.get('/book/access')
        .then(response => {
          this.issuedBooks = response.data;

          // check if the book is issued
          this.issuedBooks.forEach(accessLog => {
            if (accessLog.status === 'Issued') {
              // Fetch the rating for the book
              this.$axios.get(`/book`)
                .then(response => {
                  // add price to the issued book object
                  const book = response.data.find(book => book.id === accessLog.book_id);
                  accessLog.price = book.price;

                })
                .catch(error => {
                  console.error('Error fetching rating', error);
                });
            }
          });

        })
        .catch(error => {
          console.error('Error fetching issued books', error);
        });
    },
    submitRating(accessLog) {
      if (!accessLog.rating) {
        alert('Please select a rating before submitting.');
        return;
      }

      // Send the rating to the server
      this.$axios({
        method: 'post',
        url: `/book/rating/${accessLog.book_id}`,
        headers: {
          'Content-Type': 'application/json',
        },
        data: {
          user_id: accessLog.user_id,
          book_id: accessLog.book_id,
          rating_value: parseInt(accessLog.rating),
        },
      })
        .then(() => {
          alert('Rating submitted successfully');
          // Optionally, you can update the UI or fetch updated data
          this.fetchIssuedBooks();
        })
        .catch((error) => {
          console.error('Error submitting rating', error);
        });
    },

    deleteRequest(requestId) {
      this.$axios({
        method: 'delete',
        url: `/book/request`,
        headers: {
          'Content-Type': 'application/json',
        },
        data: {
          id: requestId,
        },
      })
        .then(response => {
          alert(response.data.message);
          this.fetchBookRequests();
        })
        .catch(error => {
          console.error('Error deleting request', error);
        });
    },

    returnBook(accessLogId) {
      this.$axios({
        method: 'put',
        url: `/book/access`,
        headers: {
          'Content-Type': 'application/json',
        },
        data: {
          id: accessLogId,
          returned: "True",
        },
      })
        .then(() => {
          // Refresh the issued books
          alert('Book returned successfully');
          this.fetchIssuedBooks();
        })
        .catch(error => {
          console.error('Error returning book', error);
        });
    },
    pdf(book_id, price) {
      //fetch all books from the server and filter the book with the given book_id and then download the pdf using the book.pdf_url
      console.log('Downloading PDF for book', book_id);
      // prompt the user to pay for the book
      if (confirm(`Do you want to buy the book for ₹${price}?`)) {
        this.$axios.get('/book')
          .then(response => {
            const books = response.data;
            const book = books.find(book => book.id === book_id);
            if (book) {
              window.open(book.pdf_url, '_blank');
            } else {
              alert('Book not found');
            }
          })
          .catch(error => {
            console.error('Error fetching books', error);
          });
      }


    },
    read(book_id) {
      //fetch all books from the server and filter the book with the given book_id and then download the pdf using the book.pdf_url
      this.$axios.get('/book')
        .then(response => {
          const books = response.data;
          const book = books.find(book => book.id === book_id);
          if (book) {
            //redirect to the book's read page with params book.epub_url
            const url = book.epub_url;
            this.$router.push({ name: 'UserRead', query: { epub_url: url } });
          } else {
            alert('Book not found');
          }
        })
        .catch(error => {
          console.error('Error fetching books', error);
        });
    },
  },
};
</script>



<style scoped>
.table {
  width: 90%;
  margin-bottom: 1rem;
  color: #10063c;
  border-collapse: collapse;
  margin: 0 auto;
}

.table th,
.table td {
  padding: 0.50rem;
  vertical-align: top;
  border-top: 5px solid #04080d;
}

.table thead th {
  vertical-align: bottom;
  border-bottom: 2px solid #25977c;
  border-top: 2px solid #25977c;
  border-left: 2px solid #25977c;
  border-right: 2px solid #25977c;
  border-style: double;
}

.table tbody+tbody {
  border-top: 2px solid #091115;
}

.table .table {
  background-color: #b01c1c;
}

.table-sm th,
.table-sm td {
  padding: 0.3rem;
}

.table-bordered {
  border: 2px solid #25977c;
}

.table-bordered th,
.table-bordered td {
  border: 2px solid #25977c;
  border-style: dashed;
}

.table-bordered thead th,
.table-bordered thead td {
  border-bottom-width: 2px;
}

.table-borderless th,
.table-borderless td,
.table-borderless thead th,
.table-borderless tbody+tbody {
  border: 0;
}

.table-striped tbody tr:nth-of-type(odd) {
  background-color: rgba(0, 0, 0, 0.05);
}

.table-hover tbody tr:hover {
  background-color: rgba(0, 0, 0, 0.075);
}

.section-title {
  background-color: #be7ebc;
  color: #5d33ba;
  padding: 6px;
  border-radius: 50px;
  width: 80%;
  margin: 0 auto;
  margin-bottom: 1rem;
  margin-top: 1rem;
}

.table-hover tbody tr:hover {
  background-color: #0f0b61;
  /* Light blue on hover */
  transition: background-color 0.3s ease-in-out;
}

.btn {
  cursor: pointer;
  transition: opacity 0.3s ease-in-out;
  border-radius: 10px;
  padding: 6px 16px;
}

.btn:hover {
  opacity: 0.8;
}

.btn-primary {
  background-color: #7db587;
  border-color: #ff00b7;
  color: #6f134f;
  font-weight: bold;
  text-align: center;
  display: inline-block;
  width: 100%;
  box-sizing: border-box;
  margin-left: auto;
}

.btn-danger {
  background-color: #35c6dc;
  border-color: #dc3545;
  color: #7b0808;
  font-weight: bold;
}

.btn-warning {
  background-color: #9b94d0;
  border-color: #35a4dc;
  color: #38087b;
  font-weight: bold;
}

.btn-secondary {
  background-color: #d69797;
  border-color: #35dc4b;
  color: #087b51;
  font-weight: bold;
}

.rating-select,
.submit-rating-btn {
  margin-right: 10px;

}

.rating-select {
  padding: 3px;
  border-radius: 10px;
  border: 2px solid #35dc4b;
  background-color: #d697bc;
  font-weight: bold;
  text-align: center;

}

.submit-rating-btn {
  font-weight: bold;
}

.returned-date {
  color: #4CAF50;
  /* Green */
  font-weight: bold;
}

.revoked-date {
  color: #ff00f2;
  /* Red */
  font-weight: bold;
}
</style>