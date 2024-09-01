variable "prod_user" {
  type    = string
  default = getenv("ATLAS_PROD_USER")
}

variable "prod_pass" {
  type    = string
  default = getenv("ATLAS_PROD_PASS")
}

variable "prod_host" {
  type    = string
  default = getenv("ATLAS_PROD_HOST")
}

data "external_schema" "sqlalchemy" {
  program = [
    "atlas-provider-sqlalchemy",
    "--path", "./db",
    "--dialect", "postgresql"
  ]
}


env "local" {
  src = "file://schema.sql"

  migration {
        dir = "file://migrations"
    }

  url = "postgres://postgres:pass@:5432/demo?search_path=public&sslmode=disable"

  dev = "docker://postgres/15/dev?search_path=public"

  format {
    migrate {
      diff = "{{ sql . \"  \" }}"
    }
  }
}

env "prod" {
  src = "file://schema.sql"

  migration {
        dir = "file://migrations"
    }

  url = "postgresql://${var.prod_user}:${var.prod_pass}@${var.prod_host}:6543/postgres?search_path=public"

  dev = "docker://postgres/15/dev?search_path=public"

  format {
    migrate {
      diff = "{{ sql . \"  \" }}"
    }
  }
}

env "sqlalchemy" {
  src = data.external_schema.sqlalchemy.url

  dev = "docker://postgres/15/dev?search_path=public"

  migration {
    dir = "file://migrations"
  }

  format {
    migrate {
      diff = "{{ sql . \"  \" }}"
    }
  }
}