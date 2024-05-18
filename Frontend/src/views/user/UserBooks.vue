<template>
  <div class="m-3">
    <!-- Recently Added Books Section -->
    <div>
      <div v-if="hasQueryParams">
        <center>
          <h1 class="mt-4">{{ search_message }}</h1>
        </center>
      </div>
      <div v-if="recentlyAdded.length && !hasQueryParams" class="mb-5">
        <hr><hr><b><center><h2><u><marquee behavior="scroll" direction="left" scrollamount="20">
          Recently Added Books
        </marquee></u></h2></center></b><hr><hr><br>
        <div class="row">
          <div v-for="book in recentlyAdded" :key="book.id" class="col-lg-2">
            <div class="card h-100">
              <img :src="book.image_url" class="card-img-top book-image" alt="Book Image" />
              <div class="card-body d-flex flex-column">
                <h5 class="card-title">{{ book.name }} </h5>
                <I>
                  Rating: {{ book.rating === 0 ? '❌ Unrated' : '⭐'.repeat(book.rating) }}
                  <p class="">
                    <span class="author-label">✍️ :</span> {{ book.author }}
                  </p>
                  <p>
                    <span class="price-label">🏷️:</span> ₹{{ book.price }} ,
                    <span>🗐 : {{ book.number_of_pages }}</span>
                  </p>
                </I>
                <p class="card-text">
                  <label for="section"><B>Description:</B></label><BR /> {{ book.content }}
                </p>
                <!-- Issue Button -->
                <div class="mt-auto">
                  <button class="btn btn-success mt-2" @click="issueBook(book)"> Request To Issue</button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div v-if="!hasQueryParams" class="mb-5">
      <hr><hr><b><center><h2><u><marquee behavior="scroll" direction="left" scrollamount="20">
        Category-Wise Books</marquee></u></h2></center></b><hr><hr>
    </div>    
        <!-- Section-wise Books Section -->
    <div v-for="(section, sectionId) in sections" :key="sectionId">
      <h3 :id=sectionId>{{ section.name }}</h3>
      <div class="row">
        <div v-for="book in section.books" :key="book.id" class="col-lg-2 col-md-4 col-sm-6 mb-4">
          <div class="card h-100">
            <img :src="book.image_url" class="card-img-top book-image" alt="Book Image" />
            <div class="card-body d-flex flex-column">
              <h5 class="card-title">{{ book.name }} </h5>
              <I>
                Rating: {{ book.rating === 0 ? '❌ Unrated' : '⭐'.repeat(book.rating) }}
                <p class="">
                  <span class="author-label">✍️ :</span> {{ book.author }}
                </p>
                <p>
                  <span class="price-label">🏷️:</span> ₹{{ book.price }} ,
                  <span>🗐 : {{ book.number_of_pages }}</span>
                </p>
              </I>
              <p class="card-text">
                <label for="section"><B>Description:</B></label><BR /> {{ book.content }}
              </p>
              <!-- Issue Button -->
              <div class="mt-auto">
                <button class="btn btn-success mt-2" @click="issueBook(book)"> Request To Issue</button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    </div>
</template>

<script>
export default {
  data() {
    return {
      sections: {},
      recentlyAdded: [],
      queryParams: this.$route.query,
      search_message: ''
    }
  },

  mounted() {
    this.getBooks()
  },
  computed: {
    hasQueryParams() {
      // Check if queryParams exist
      if (Object.keys(this.queryParams).length > 0) {
        const key = Object.keys(this.queryParams)[0];
        const value = this.queryParams[key];

        console.log(key, value);

        if (key === 'category') {


          this.search_message = ``;
          return true;
        } else if (key === 'author') {
          // Scroll to the section with id equal to the author value

          this.search_message = `Books by Author ${value}`;
          return true;
        } else if (key === 'name') {
          // Scroll to the section with id equal to the name value

          this.search_message = `Books with Name ${value}`;
          return true;
        } else {
          console.log("Invalid query parameter");
          return false;
        }
      } else {
        console.log("No query parameters found.");
        return false;
      }
    },
  },
  methods: {
    async getBooks() {
      try {
        const bookResponse = await this.$axios.get('/book');
        const sectionResponse = await this.$axios.get('/section');

        this.processBooks(bookResponse.data, sectionResponse.data, this.$route.query);
        this.sortRecentlyAdded(bookResponse.data);
      } catch (error) {
        console.error('Error fetching books:', error);
      }
    },
    sortRecentlyAdded(books) {
      // Sort and limit to 5 recently added books that is last 5 books and convert book object to array
      this.recentlyAdded = Object.values(books)
        .sort((a, b) => b.id - a.id)
        .slice(0, 5);
    },
    processBooks(books, sections, queryParams) {
      this.sections = {};

      for (const section of Object.values(sections)) {
        const sectionId = section.id.toString();
        this.sections[sectionId] = {
          name: section.name,
          books: []
        };
      }

      for (const book of Object.values(books)) {
        const sectionId = book.section_id.toString();

        // Check if the book matches the filter criteria based on query parameters
        if (
          (!queryParams.category || book.section_id === parseInt(queryParams.category)) &&
          (!queryParams.author || book.author.toLowerCase().includes(queryParams.author.toLowerCase())) &&
          (!queryParams.name || book.name.toLowerCase().includes(queryParams.name.toLowerCase()))
        ) {
          if (this.sections[sectionId]) {
            this.sections[sectionId].books.push({
              id: book.id,
              name: book.name,
              author: book.author,
              price: book.price,
              image_url: book.image_url,
              category: book.category,
              number_of_pages: book.number_of_pages,
              rating: book.rating,
              content: book.content
            });
          }
        }
      }

      // Remove empty categories from sections
      for (const sectionId in this.sections) {
        if (this.sections[sectionId].books.length === 0) {
          delete this.sections[sectionId];
        }
      }
    }


    ,
    issueBook(book) {
      // Implement issue book logic here
      (async () => {
        try {
          await this.$axios.post('/book/request', {
            book_id: book.id,
            user_id: localStorage.getItem('user_id'),
          }).then((response) => {
            console.log(response);
            alert(response.data.message);
          });
          // Handle success
        } catch (error) {
          console.error('Error issuing book:', error);
        }
      })();
    }
  }
}
</script>

<style scoped>
.book-image {
  height: 200px;
  object-fit: cover;
}

.author-label {
  font-size: 1.2rem;
}

.price-label {
  font-size: 1.2rem;
}
</style>
