package serializers

type QueryParamSerializer struct {
	Page     int32 `validate:"gte=1" query:"page"`
	PageSize int32 `validate:"gte=1" query:"pageSize"`
}
