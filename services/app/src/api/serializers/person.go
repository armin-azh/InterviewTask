package serializers

type PersonSerializer struct {
	FirstName string `validate:"required,min=5,max=50" json:"first_name"`
	LastName  string `validate:"required,min=5,max=50" json:"last_name"`
}
