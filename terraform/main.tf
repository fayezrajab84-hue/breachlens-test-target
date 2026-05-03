# Intentionally insecure Terraform for BreachLens IaC scanner (Checkov)
# DO NOT APPLY — every resource here exists to trigger a known check.

# ── S3 misconfigurations ──────────────────────────────────────────────
resource "aws_s3_bucket" "public_data" {
  bucket = "my-public-data-bucket"
  # CKV_AWS_20: S3 bucket should not be public
  acl    = "public-read"
}

resource "aws_s3_bucket" "no_versioning" {
  bucket = "my-no-versioning-bucket"
  # CKV_AWS_21: S3 bucket should have versioning enabled (missing)
  # CKV_AWS_18: S3 bucket should have access logging (missing)
}

# ── Security group wide open to internet ──────────────────────────────
resource "aws_security_group" "wide_open" {
  name        = "wide-open-sg"
  description = "DEMO ONLY — allow everything from anywhere"

  ingress {
    description = "All traffic from anywhere"
    from_port   = 0
    to_port     = 65535
    protocol    = "-1"
    # CKV_AWS_24: Ensure no security groups allow ingress from 0.0.0.0/0 to port 22
    # CKV_AWS_260: Ensure no security groups allow ingress from 0.0.0.0/0 to port 80
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# ── RDS instance with multiple misconfigs ─────────────────────────────
resource "aws_db_instance" "insecure_db" {
  identifier              = "demo-db"
  engine                  = "mysql"
  engine_version          = "5.7"
  instance_class          = "db.t3.micro"
  allocated_storage       = 20
  username                = "admin"
  password                = random_password.db_password.result
  # CKV_AWS_16: RDS instance should have storage encryption enabled
  storage_encrypted       = false
  # CKV_AWS_17: RDS instance should NOT be publicly accessible
  publicly_accessible     = true
  # CKV_AWS_133: RDS should have backup retention period
  backup_retention_period = 0
  # CKV_AWS_293: RDS instance should have deletion protection
  deletion_protection     = false
  # CKV_AWS_354: RDS should have IAM authentication enabled
  iam_database_authentication_enabled = false
  skip_final_snapshot     = true
}

# ── EC2 with no IMDSv2 enforcement ────────────────────────────────────
resource "aws_instance" "demo_ec2" {
  ami           = "ami-0c55b159cbfafe1f0"
  instance_type = "t3.micro"

  # CKV_AWS_79: EC2 should require IMDSv2 (token) — http_tokens="required"
  metadata_options {
    http_tokens = "optional"
  }

  # CKV_AWS_135: EC2 instance should be EBS-optimized
  ebs_optimized = false

  # CKV_AWS_8: EBS should be encrypted
  root_block_device {
    encrypted = false
  }

  vpc_security_group_ids = [aws_security_group.wide_open.id]
}

# ── IAM policy with admin access ──────────────────────────────────────
resource "aws_iam_policy" "admin_everything" {
  name = "admin-everything"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      # CKV_AWS_62: IAM policies should not allow full administrative privileges
      # CKV_AWS_63: IAM policies should not allow Action: "*" + Resource: "*"
      Effect   = "Allow"
      Action   = "*"
      Resource = "*"
    }]
  })
}
