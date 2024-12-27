<template>
  <el-container>
    <!-- Header -->
    <el-header>
      <h1 style="color: white; text-align: center;">My Element UI App</h1>
    </el-header>

    <!-- Main Content -->
    <el-container>
      <el-aside width="200px">
        <el-menu default-active="1" class="el-menu-vertical-demo">
          <el-menu-item index="1">Dashboard</el-menu-item>
          <el-menu-item index="2">Settings</el-menu-item>
          <el-menu-item index="3">Profile</el-menu-item>
        </el-menu>
      </el-aside>

      <el-main>
        <!-- Form -->
        <el-form :model="form" label-width="120px" @submit.prevent="onSubmit">
          <el-form-item label="Name">
            <el-input v-model="form.name" placeholder="Enter your name"></el-input>
          </el-form-item>
          <el-form-item label="Email">
            <el-input v-model="form.email" placeholder="Enter your email"></el-input>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="onSubmit">Submit</el-button>
          </el-form-item>
        </el-form>

        <!-- Table -->
        <el-table :data="tableData" style="width: 100%">
          <el-table-column prop="name" label="Name" width="180"></el-table-column>
          <el-table-column prop="email" label="Email" width="200"></el-table-column>
          <el-table-column label="Actions" width="150">
            <template #default="scope">
              <el-button size="small" type="primary" @click="openDialog(scope.row)">
                Edit
              </el-button>
            </template>
          </el-table-column>
        </el-table>

        <!-- Dialog -->
        <el-dialog title="Edit User" v-model="dialogVisible">
          <el-form :model="editForm">
            <el-form-item label="Name">
              <el-input v-model="editForm.name"></el-input>
            </el-form-item>
            <el-form-item label="Email">
              <el-input v-model="editForm.email"></el-input>
            </el-form-item>
          </el-form>
          <div>
            <el-button @click="dialogVisible = false">Cancel</el-button>
            <el-button type="primary" @click="saveEdit">Save</el-button>
          </div>
        </el-dialog>
      </el-main>
    </el-container>
  </el-container>
</template>

<script>
export default {
  data() {
    return {
      form: {
        name: '',
        email: '',
      },
      tableData: [
        { name: 'John Doe', email: 'john@example.com' },
        { name: 'Jane Smith', email: 'jane@example.com' },
      ],
      dialogVisible: false,
      editForm: {
        name: '',
        email: '',
      },
    };
  },
  methods: {
    onSubmit() {
      this.tableData.push({ ...this.form });
      this.form.name = '';
      this.form.email = '';
    },
    openDialog(row) {
      this.editForm = { ...row };
      this.dialogVisible = true;
    },
    saveEdit() {
      const index = this.tableData.findIndex(
        (item) => item.email === this.editForm.email
      );
      if (index !== -1) {
        this.tableData[index] = { ...this.editForm };
      }
      this.dialogVisible = false;
    },
  },
};
</script>

<style>
h1 {
  margin: 0;
  padding: 0.5rem 0;
}
</style>
