# --------------------------------------------------------------------------
# ⚠️ WARNING - AUTO-GENERATED CODE - DO NOT EDIT ⚠️
# ⚙️ Generated by 'python -m opgen'
# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
# --------------------------------------------------------------------------
# pylint: disable=W0221,W0222,R0901,W0237
# mypy: disable-error-code=override
# ruff: noqa: N801,E741
# ruff: noqa: D214,D402,D405,D411,D412,D416,D417
# --------------------------------------------------------------------------

from __future__ import annotations

from typing import Mapping, Optional, Sequence, Tuple, TypeVar, Union

from onnx.defs import get_schema
from typing_extensions import TypeAlias

from onnxscript.onnx_types import DOUBLE, FLOAT, INT32, INT64, STRING
from onnxscript.values import Op, Opset


class Opset_ai_onnx_ml1(Opset):
    def __new__(cls):
        return Opset.__new__(cls, "ai.onnx.ml", 1)

    T_ArrayFeatureExtractor = TypeVar(
        "T_ArrayFeatureExtractor", DOUBLE, FLOAT, INT32, INT64, STRING
    )

    def ArrayFeatureExtractor(
        self, X: T_ArrayFeatureExtractor, Y: INT64
    ) -> T_ArrayFeatureExtractor:
        r"""[🌐 ai.onnx.ml::ArrayFeatureExtractor(1)](https://onnx.ai/onnx/operators/onnx_aionnxml_ArrayFeatureExtractor.html#arrayfeatureextractor-1 "Online Documentation")


            Select elements of the input tensor based on the indices passed.

            The indices are applied to the last axes of the tensor.


        Args:
            X: Data to be selected

            Y: The indices, based on 0 as the first index of any dimension.
        """

        schema = get_schema("ArrayFeatureExtractor", 1, "ai.onnx.ml")
        op = Op(self, "ArrayFeatureExtractor", schema)
        return op(*self._prepare_inputs(schema, X, Y))

    T_Binarizer = TypeVar("T_Binarizer", DOUBLE, FLOAT, INT32, INT64)

    def Binarizer(self, X: T_Binarizer, *, threshold: float = 0.0) -> T_Binarizer:
        r"""[🌐 ai.onnx.ml::Binarizer(1)](https://onnx.ai/onnx/operators/onnx_aionnxml_Binarizer.html#binarizer-1 "Online Documentation")


            Maps the values of the input tensor to either 0 or 1, element-wise, based on the outcome of a comparison against a threshold value.


        Args:
            X: Data to be binarized

            threshold: Values greater than this are mapped to 1, others to 0.
        """

        schema = get_schema("Binarizer", 1, "ai.onnx.ml")
        op = Op(self, "Binarizer", schema)
        return op(*self._prepare_inputs(schema, X), threshold=threshold)

    T1_CastMap = TypeVar("T1_CastMap", Mapping[int, FLOAT], Mapping[int, STRING])

    T2_CastMap: TypeAlias = Union[FLOAT, INT64, STRING]

    def CastMap(
        self,
        X: T1_CastMap,
        *,
        cast_to: str = "TO_FLOAT",
        map_form: str = "DENSE",
        max_map: int = 1,
    ) -> T2_CastMap:
        r"""[🌐 ai.onnx.ml::CastMap(1)](https://onnx.ai/onnx/operators/onnx_aionnxml_CastMap.html#castmap-1 "Online Documentation")


            Converts a map to a tensor.
        The map key must be an int64 and the values will be ordered
            in ascending order based on this key.
        The operator supports dense packing or sparse packing.
            If using sparse packing, the key cannot exceed the max_map-1 value.


        Args:
            X: The input map that is to be cast to a tensor

            cast_to: A string indicating the desired element type of the output tensor,
                one of 'TO_FLOAT', 'TO_STRING', 'TO_INT64'.

            map_form: Indicates whether to only output as many values as are in the
                input (dense), or position the input based on using the key of the map
                as the index of the output (sparse).<br>One of 'DENSE', 'SPARSE'.

            max_map: If the value of map_form is 'SPARSE,' this attribute indicates the
                total length of the output tensor.
        """

        schema = get_schema("CastMap", 1, "ai.onnx.ml")
        op = Op(self, "CastMap", schema)
        return op(
            *self._prepare_inputs(schema, X),
            cast_to=cast_to,
            map_form=map_form,
            max_map=max_map,
        )

    T1_CategoryMapper = TypeVar("T1_CategoryMapper", INT64, STRING)

    T2_CategoryMapper: TypeAlias = Union[INT64, STRING]

    def CategoryMapper(
        self,
        X: T1_CategoryMapper,
        *,
        cats_int64s: Optional[Sequence[int]] = None,
        cats_strings: Optional[Sequence[str]] = None,
        default_int64: int = -1,
        default_string: str = "_Unused",
    ) -> T2_CategoryMapper:
        r"""[🌐 ai.onnx.ml::CategoryMapper(1)](https://onnx.ai/onnx/operators/onnx_aionnxml_CategoryMapper.html#categorymapper-1 "Online Documentation")


            Converts strings to integers and vice versa.

            Two sequences of equal length are used to map between integers and strings,
            with strings and integers at the same index detailing the mapping.

            Each operator converts either integers to strings or strings to integers, depending
            on which default value attribute is provided. Only one default value attribute
            should be defined.

            If the string default value is set, it will convert integers to strings.
            If the int default value is set, it will convert strings to integers.


        Args:
            X: Input data

            cats_int64s: The integers of the map. This sequence must be the same length
                as the 'cats_strings' sequence.

            cats_strings: The strings of the map. This sequence must be the same length
                as the 'cats_int64s' sequence

            default_int64: An integer to use when an input string value is not found in
                the map.<br>One and only one of the 'default_*' attributes must be
                defined.

            default_string: A string to use when an input integer value is not found in
                the map.<br>One and only one of the 'default_*' attributes must be
                defined.
        """

        schema = get_schema("CategoryMapper", 1, "ai.onnx.ml")
        op = Op(self, "CategoryMapper", schema)
        return op(
            *self._prepare_inputs(schema, X),
            cats_int64s=cats_int64s,
            cats_strings=cats_strings,
            default_int64=default_int64,
            default_string=default_string,
        )

    T1_DictVectorizer = TypeVar(
        "T1_DictVectorizer",
        Mapping[int, DOUBLE],
        Mapping[int, FLOAT],
        Mapping[int, STRING],
        Mapping[str, DOUBLE],
        Mapping[str, FLOAT],
        Mapping[str, INT64],
    )

    T2_DictVectorizer: TypeAlias = Union[DOUBLE, FLOAT, INT64, STRING]

    def DictVectorizer(
        self,
        X: T1_DictVectorizer,
        *,
        int64_vocabulary: Optional[Sequence[int]] = None,
        string_vocabulary: Optional[Sequence[str]] = None,
    ) -> T2_DictVectorizer:
        r"""[🌐 ai.onnx.ml::DictVectorizer(1)](https://onnx.ai/onnx/operators/onnx_aionnxml_DictVectorizer.html#dictvectorizer-1 "Online Documentation")


            Uses an index mapping to convert a dictionary to an array.

            Given a dictionary, each key is looked up in the vocabulary attribute corresponding to
            the key type. The index into the vocabulary array at which the key is found is then
            used to index the output 1-D tensor 'Y' and insert into it the value found in the dictionary 'X'.

            The key type of the input map must correspond to the element type of the defined vocabulary attribute.
            Therefore, the output array will be equal in length to the index mapping vector parameter.
            All keys in the input dictionary must be present in the index mapping vector.
            For each item in the input dictionary, insert its value in the output array.
            Any keys not present in the input dictionary, will be zero in the output array.

            For example: if the ``string_vocabulary`` parameter is set to ``["a", "c", "b", "z"]``,
            then an input of ``{"a": 4, "c": 8}`` will produce an output of ``[4, 8, 0, 0]``.


        Args:
            X: A dictionary.

            int64_vocabulary: An integer vocabulary array.<br>One and only one of the
                vocabularies must be defined.

            string_vocabulary: A string vocabulary array.<br>One and only one of the
                vocabularies must be defined.
        """

        schema = get_schema("DictVectorizer", 1, "ai.onnx.ml")
        op = Op(self, "DictVectorizer", schema)
        return op(
            *self._prepare_inputs(schema, X),
            int64_vocabulary=int64_vocabulary,
            string_vocabulary=string_vocabulary,
        )

    T1_FeatureVectorizer = TypeVar("T1_FeatureVectorizer", DOUBLE, FLOAT, INT32, INT64)

    def FeatureVectorizer(
        self, *X: T1_FeatureVectorizer, inputdimensions: Optional[Sequence[int]] = None
    ) -> FLOAT:
        r"""[🌐 ai.onnx.ml::FeatureVectorizer(1)](https://onnx.ai/onnx/operators/onnx_aionnxml_FeatureVectorizer.html#featurevectorizer-1 "Online Documentation")


            Concatenates input tensors into one continuous output.

            All input shapes are 2-D and are concatenated along the second dimention. 1-D tensors are treated as [1,C].
            Inputs are copied to the output maintaining the order of the input arguments.

            All inputs must be integers or floats, while the output will be all floating point values.


        Args:
            X: (variadic) An ordered collection of tensors, all with the same element
                type.

            inputdimensions: The size of each input in the input list
        """

        schema = get_schema("FeatureVectorizer", 1, "ai.onnx.ml")
        op = Op(self, "FeatureVectorizer", schema)
        return op(*self._prepare_inputs(schema, *X), inputdimensions=inputdimensions)

    T_Imputer = TypeVar("T_Imputer", DOUBLE, FLOAT, INT32, INT64)

    def Imputer(
        self,
        X: T_Imputer,
        *,
        imputed_value_floats: Optional[Sequence[float]] = None,
        imputed_value_int64s: Optional[Sequence[int]] = None,
        replaced_value_float: float = 0.0,
        replaced_value_int64: int = 0,
    ) -> T_Imputer:
        r"""[🌐 ai.onnx.ml::Imputer(1)](https://onnx.ai/onnx/operators/onnx_aionnxml_Imputer.html#imputer-1 "Online Documentation")


            Replaces inputs that equal one value with another, leaving all other elements alone.

            This operator is typically used to replace missing values in situations where they have a canonical
            representation, such as -1, 0, NaN, or some extreme value.

            One and only one of imputed_value_floats or imputed_value_int64s should be defined -- floats if the input tensor
            holds floats, integers if the input tensor holds integers. The imputed values must all fit within the
            width of the tensor element type. One and only one of the replaced_value_float or replaced_value_int64 should be defined,
            which one depends on whether floats or integers are being processed.

            The imputed_value attribute length can be 1 element, or it can have one element per input feature.
        In other words, if the input tensor has the shape [*,F], then the length of the attribute array may be 1 or F. If it is 1, then it is broadcast along the last dimension and applied to each feature.


        Args:
            X: Data to be processed.

            imputed_value_floats: Value(s) to change to

            imputed_value_int64s: Value(s) to change to.

            replaced_value_float: A value that needs replacing.

            replaced_value_int64: A value that needs replacing.
        """

        schema = get_schema("Imputer", 1, "ai.onnx.ml")
        op = Op(self, "Imputer", schema)
        return op(
            *self._prepare_inputs(schema, X),
            imputed_value_floats=imputed_value_floats,
            imputed_value_int64s=imputed_value_int64s,
            replaced_value_float=replaced_value_float,
            replaced_value_int64=replaced_value_int64,
        )

    T1_LabelEncoder = TypeVar("T1_LabelEncoder", INT64, STRING)

    T2_LabelEncoder: TypeAlias = Union[INT64, STRING]

    def LabelEncoder(
        self,
        X: T1_LabelEncoder,
        *,
        classes_strings: Optional[Sequence[str]] = None,
        default_int64: int = -1,
        default_string: str = "_Unused",
    ) -> T2_LabelEncoder:
        r"""[🌐 ai.onnx.ml::LabelEncoder(1)](https://onnx.ai/onnx/operators/onnx_aionnxml_LabelEncoder.html#labelencoder-1 "Online Documentation")


            Converts strings to integers and vice versa.

            If the string default value is set, it will convert integers to strings.
            If the int default value is set, it will convert strings to integers.

            Each operator converts either integers to strings or strings to integers, depending
            on which default value attribute is provided. Only one default value attribute
            should be defined.

            When converting from integers to strings, the string is fetched from the
            'classes_strings' list, by simple indexing.

            When converting from strings to integers, the string is looked up in the list
            and the index at which it is found is used as the converted value.


        Args:
            X: Input data.

            classes_strings: A list of labels.

            default_int64: An integer to use when an input string value is not found in
                the map.<br>One and only one of the 'default_*' attributes must be
                defined.

            default_string: A string to use when an input integer value is not found in
                the map.<br>One and only one of the 'default_*' attributes must be
                defined.
        """

        schema = get_schema("LabelEncoder", 1, "ai.onnx.ml")
        op = Op(self, "LabelEncoder", schema)
        return op(
            *self._prepare_inputs(schema, X),
            classes_strings=classes_strings,
            default_int64=default_int64,
            default_string=default_string,
        )

    T1_LinearClassifier = TypeVar("T1_LinearClassifier", DOUBLE, FLOAT, INT32, INT64)

    T2_LinearClassifier: TypeAlias = Union[INT64, STRING]

    def LinearClassifier(
        self,
        X: T1_LinearClassifier,
        *,
        classlabels_ints: Optional[Sequence[int]] = None,
        classlabels_strings: Optional[Sequence[str]] = None,
        coefficients: Sequence[float],
        intercepts: Optional[Sequence[float]] = None,
        multi_class: int = 0,
        post_transform: str = "NONE",
    ) -> Tuple[T2_LinearClassifier, FLOAT]:
        r"""[🌐 ai.onnx.ml::LinearClassifier(1)](https://onnx.ai/onnx/operators/onnx_aionnxml_LinearClassifier.html#linearclassifier-1 "Online Documentation")


            Linear classifier


        Args:
            X: Data to be classified.

            classlabels_ints: Class labels when using integer labels. One and only one
                'classlabels' attribute must be defined.

            classlabels_strings: Class labels when using string labels. One and only one
                'classlabels' attribute must be defined.

            coefficients: A collection of weights of the model(s).

            intercepts: A collection of intercepts.

            multi_class: Indicates whether to do OvR or multinomial (0=OvR is the
                default).

            post_transform: Indicates the transform to apply to the scores
                vector.<br>One of 'NONE,' 'SOFTMAX,' 'LOGISTIC,' 'SOFTMAX_ZERO,' or
                'PROBIT'
        """

        schema = get_schema("LinearClassifier", 1, "ai.onnx.ml")
        op = Op(self, "LinearClassifier", schema)
        return op(
            *self._prepare_inputs(schema, X),
            classlabels_ints=classlabels_ints,
            classlabels_strings=classlabels_strings,
            coefficients=coefficients,
            intercepts=intercepts,
            multi_class=multi_class,
            post_transform=post_transform,
        )

    T_LinearRegressor = TypeVar("T_LinearRegressor", DOUBLE, FLOAT, INT32, INT64)

    def LinearRegressor(
        self,
        X: T_LinearRegressor,
        *,
        coefficients: Optional[Sequence[float]] = None,
        intercepts: Optional[Sequence[float]] = None,
        post_transform: str = "NONE",
        targets: int = 1,
    ) -> FLOAT:
        r"""[🌐 ai.onnx.ml::LinearRegressor(1)](https://onnx.ai/onnx/operators/onnx_aionnxml_LinearRegressor.html#linearregressor-1 "Online Documentation")


            Generalized linear regression evaluation.

            If targets is set to 1 (default) then univariate regression is performed.

            If targets is set to M then M sets of coefficients must be passed in as a sequence
            and M results will be output for each input n in N.

            The coefficients array is of length n, and the coefficients for each target are contiguous.
            Intercepts are optional but if provided must match the number of targets.


        Args:
            X: Data to be regressed.

            coefficients: Weights of the model(s).

            intercepts: Weights of the intercepts, if used.

            post_transform: Indicates the transform to apply to the regression output
                vector.<br>One of 'NONE,' 'SOFTMAX,' 'LOGISTIC,' 'SOFTMAX_ZERO,' or
                'PROBIT'

            targets: The total number of regression targets, 1 if not defined.
        """

        schema = get_schema("LinearRegressor", 1, "ai.onnx.ml")
        op = Op(self, "LinearRegressor", schema)
        return op(
            *self._prepare_inputs(schema, X),
            coefficients=coefficients,
            intercepts=intercepts,
            post_transform=post_transform,
            targets=targets,
        )

    T_Normalizer = TypeVar("T_Normalizer", DOUBLE, FLOAT, INT32, INT64)

    def Normalizer(self, X: T_Normalizer, *, norm: str = "MAX") -> FLOAT:
        r"""[🌐 ai.onnx.ml::Normalizer(1)](https://onnx.ai/onnx/operators/onnx_aionnxml_Normalizer.html#normalizer-1 "Online Documentation")


            Normalize the input.  There are three normalization modes, which have the corresponding formulas,
            defined using element-wise infix operators '/' and '^' and tensor-wide functions 'max' and 'sum':



            Max: Y = X / max(X)

            L1:  Y = X / sum(X)

            L2:  Y = sqrt(X^2 / sum(X^2)}

            In all modes, if the divisor is zero, Y == X.


            For batches, that is, [N,C] tensors, normalization is done along the C axis. In other words, each row
            of the batch is normalized independently.


        Args:
            X: Data to be encoded, a tensor of shape [N,C] or [C]

            norm: One of 'MAX,' 'L1,' 'L2'
        """

        schema = get_schema("Normalizer", 1, "ai.onnx.ml")
        op = Op(self, "Normalizer", schema)
        return op(*self._prepare_inputs(schema, X), norm=norm)

    T_OneHotEncoder = TypeVar("T_OneHotEncoder", DOUBLE, FLOAT, INT32, INT64, STRING)

    def OneHotEncoder(
        self,
        X: T_OneHotEncoder,
        *,
        cats_int64s: Optional[Sequence[int]] = None,
        cats_strings: Optional[Sequence[str]] = None,
        zeros: int = 1,
    ) -> FLOAT:
        r"""[🌐 ai.onnx.ml::OneHotEncoder(1)](https://onnx.ai/onnx/operators/onnx_aionnxml_OneHotEncoder.html#onehotencoder-1 "Online Documentation")


            Replace each input element with an array of ones and zeros, where a single
            one is placed at the index of the category that was passed in. The total category count
            will determine the size of the extra dimension of the output array Y.

            For example, if we pass a tensor with a single value of 4, and a category count of 8,
            the output will be a tensor with ``[0,0,0,0,1,0,0,0]``.

            This operator assumes every input feature is from the same set of categories.

            If the input is a tensor of float, int32, or double, the data will be cast
            to integers and the cats_int64s category list will be used for the lookups.


        Args:
            X: Data to be encoded.

            cats_int64s: List of categories, ints.<br>One and only one of the 'cats_*'
                attributes must be defined.

            cats_strings: List of categories, strings.<br>One and only one of the
                'cats_*' attributes must be defined.

            zeros: If true and category is not present, will return all zeros; if false
                and a category if not found, the operator will fail.
        """

        schema = get_schema("OneHotEncoder", 1, "ai.onnx.ml")
        op = Op(self, "OneHotEncoder", schema)
        return op(
            *self._prepare_inputs(schema, X),
            cats_int64s=cats_int64s,
            cats_strings=cats_strings,
            zeros=zeros,
        )

    T1_SVMClassifier = TypeVar("T1_SVMClassifier", DOUBLE, FLOAT, INT32, INT64)

    T2_SVMClassifier: TypeAlias = Union[INT64, STRING]

    def SVMClassifier(
        self,
        X: T1_SVMClassifier,
        *,
        classlabels_ints: Optional[Sequence[int]] = None,
        classlabels_strings: Optional[Sequence[str]] = None,
        coefficients: Optional[Sequence[float]] = None,
        kernel_params: Optional[Sequence[float]] = None,
        kernel_type: str = "LINEAR",
        post_transform: str = "NONE",
        prob_a: Optional[Sequence[float]] = None,
        prob_b: Optional[Sequence[float]] = None,
        rho: Optional[Sequence[float]] = None,
        support_vectors: Optional[Sequence[float]] = None,
        vectors_per_class: Optional[Sequence[int]] = None,
    ) -> Tuple[T2_SVMClassifier, FLOAT]:
        r"""[🌐 ai.onnx.ml::SVMClassifier(1)](https://onnx.ai/onnx/operators/onnx_aionnxml_SVMClassifier.html#svmclassifier-1 "Online Documentation")


            Support Vector Machine classifier


        Args:
            X: Data to be classified.

            classlabels_ints: Class labels if using integer labels.<br>One and only one
                of the 'classlabels_*' attributes must be defined.

            classlabels_strings: Class labels if using string labels.<br>One and only
                one of the 'classlabels_*' attributes must be defined.

            kernel_params: List of 3 elements containing gamma, coef0, and degree, in
                that order. Zero if unused for the kernel.

            kernel_type: The kernel type, one of 'LINEAR,' 'POLY,' 'RBF,' 'SIGMOID'.

            post_transform: Indicates the transform to apply to the score. <br>One of
                'NONE,' 'SOFTMAX,' 'LOGISTIC,' 'SOFTMAX_ZERO,' or 'PROBIT'

            prob_a: First set of probability coefficients.

            prob_b: Second set of probability coefficients. This array must be same size
                as prob_a.<br>If these are provided then output Z are probability
                estimates, otherwise they are raw scores.
        """

        schema = get_schema("SVMClassifier", 1, "ai.onnx.ml")
        op = Op(self, "SVMClassifier", schema)
        return op(
            *self._prepare_inputs(schema, X),
            classlabels_ints=classlabels_ints,
            classlabels_strings=classlabels_strings,
            coefficients=coefficients,
            kernel_params=kernel_params,
            kernel_type=kernel_type,
            post_transform=post_transform,
            prob_a=prob_a,
            prob_b=prob_b,
            rho=rho,
            support_vectors=support_vectors,
            vectors_per_class=vectors_per_class,
        )

    T_SVMRegressor = TypeVar("T_SVMRegressor", DOUBLE, FLOAT, INT32, INT64)

    def SVMRegressor(
        self,
        X: T_SVMRegressor,
        *,
        coefficients: Optional[Sequence[float]] = None,
        kernel_params: Optional[Sequence[float]] = None,
        kernel_type: str = "LINEAR",
        n_supports: int = 0,
        one_class: int = 0,
        post_transform: str = "NONE",
        rho: Optional[Sequence[float]] = None,
        support_vectors: Optional[Sequence[float]] = None,
    ) -> FLOAT:
        r"""[🌐 ai.onnx.ml::SVMRegressor(1)](https://onnx.ai/onnx/operators/onnx_aionnxml_SVMRegressor.html#svmregressor-1 "Online Documentation")


            Support Vector Machine regression prediction and one-class SVM anomaly detection.


        Args:
            X: Data to be regressed.

            coefficients: Support vector coefficients.

            kernel_params: List of 3 elements containing gamma, coef0, and degree, in
                that order. Zero if unused for the kernel.

            kernel_type: The kernel type, one of 'LINEAR,' 'POLY,' 'RBF,' 'SIGMOID'.

            n_supports: The number of support vectors.

            one_class: Flag indicating whether the regression is a one-class SVM or not.

            post_transform: Indicates the transform to apply to the score. <br>One of
                'NONE,' 'SOFTMAX,' 'LOGISTIC,' 'SOFTMAX_ZERO,' or 'PROBIT.'

            support_vectors: Chosen support vectors
        """

        schema = get_schema("SVMRegressor", 1, "ai.onnx.ml")
        op = Op(self, "SVMRegressor", schema)
        return op(
            *self._prepare_inputs(schema, X),
            coefficients=coefficients,
            kernel_params=kernel_params,
            kernel_type=kernel_type,
            n_supports=n_supports,
            one_class=one_class,
            post_transform=post_transform,
            rho=rho,
            support_vectors=support_vectors,
        )

    T_Scaler = TypeVar("T_Scaler", DOUBLE, FLOAT, INT32, INT64)

    def Scaler(
        self,
        X: T_Scaler,
        *,
        offset: Optional[Sequence[float]] = None,
        scale: Optional[Sequence[float]] = None,
    ) -> FLOAT:
        r"""[🌐 ai.onnx.ml::Scaler(1)](https://onnx.ai/onnx/operators/onnx_aionnxml_Scaler.html#scaler-1 "Online Documentation")


            Rescale input data, for example to standardize features by removing the mean and scaling to unit variance.


        Args:
            X: Data to be scaled.

            offset: First, offset by this.<br>Can be length of features in an [N,F]
                tensor or length 1, in which case it applies to all features, regardless
                of dimension count.

            scale: Second, multiply by this.<br>Can be length of features in an [N,F]
                tensor or length 1, in which case it applies to all features, regardless
                of dimension count.<br>Must be same length as 'offset'
        """

        schema = get_schema("Scaler", 1, "ai.onnx.ml")
        op = Op(self, "Scaler", schema)
        return op(*self._prepare_inputs(schema, X), offset=offset, scale=scale)

    T1_TreeEnsembleClassifier = TypeVar(
        "T1_TreeEnsembleClassifier", DOUBLE, FLOAT, INT32, INT64
    )

    T2_TreeEnsembleClassifier: TypeAlias = Union[INT64, STRING]

    def TreeEnsembleClassifier(
        self,
        X: T1_TreeEnsembleClassifier,
        *,
        base_values: Optional[Sequence[float]] = None,
        class_ids: Optional[Sequence[int]] = None,
        class_nodeids: Optional[Sequence[int]] = None,
        class_treeids: Optional[Sequence[int]] = None,
        class_weights: Optional[Sequence[float]] = None,
        classlabels_int64s: Optional[Sequence[int]] = None,
        classlabels_strings: Optional[Sequence[str]] = None,
        nodes_falsenodeids: Optional[Sequence[int]] = None,
        nodes_featureids: Optional[Sequence[int]] = None,
        nodes_hitrates: Optional[Sequence[float]] = None,
        nodes_missing_value_tracks_true: Optional[Sequence[int]] = None,
        nodes_modes: Optional[Sequence[str]] = None,
        nodes_nodeids: Optional[Sequence[int]] = None,
        nodes_treeids: Optional[Sequence[int]] = None,
        nodes_truenodeids: Optional[Sequence[int]] = None,
        nodes_values: Optional[Sequence[float]] = None,
        post_transform: str = "NONE",
    ) -> Tuple[T2_TreeEnsembleClassifier, FLOAT]:
        r"""[🌐 ai.onnx.ml::TreeEnsembleClassifier(1)](https://onnx.ai/onnx/operators/onnx_aionnxml_TreeEnsembleClassifier.html#treeensembleclassifier-1 "Online Documentation")


            Tree Ensemble classifier.  Returns the top class for each of N inputs.

            The attributes named 'nodes_X' form a sequence of tuples, associated by
            index into the sequences, which must all be of equal length. These tuples
            define the nodes.

            Similarly, all fields prefixed with 'class_' are tuples of votes at the leaves.
            A leaf may have multiple votes, where each vote is weighted by
            the associated class_weights index.

            One and only one of classlabels_strings or classlabels_int64s
            will be defined. The class_ids are indices into this list.


        Args:
            X: Input of shape [N,F]

            base_values: Base values for classification, added to final class score; the
                size must be the same as the classes or can be left unassigned (assumed
                0)

            class_ids: The index of the class list that each weight is for.

            class_nodeids: node id that this weight is for.

            class_treeids: The id of the tree that this node is in.

            class_weights: The weight for the class in class_id.

            classlabels_int64s: Class labels if using integer labels.<br>One and only
                one of the 'classlabels_*' attributes must be defined.

            classlabels_strings: Class labels if using string labels.<br>One and only
                one of the 'classlabels_*' attributes must be defined.

            nodes_falsenodeids: Child node if expression is false.

            nodes_featureids: Feature id for each node.

            nodes_hitrates: Popularity of each node, used for performance and may be
                omitted.

            nodes_missing_value_tracks_true: For each node, define what to do in the
                presence of a missing value: if a value is missing (NaN), use the 'true'
                or 'false' branch based on the value in this array.<br>This attribute
                may be left undefined, and the defalt value is false (0) for all nodes.

            nodes_modes: The node kind, that is, the comparison to make at the node.
                There is no comparison to make at a leaf node.<br>One of 'BRANCH_LEQ',
                'BRANCH_LT', 'BRANCH_GTE', 'BRANCH_GT', 'BRANCH_EQ', 'BRANCH_NEQ',
                'LEAF'

            nodes_nodeids: Node id for each node. Ids may restart at zero for each tree,
                but it not required to.

            nodes_treeids: Tree id for each node.

            nodes_truenodeids: Child node if expression is true.

            nodes_values: Thresholds to do the splitting on for each node.

            post_transform: Indicates the transform to apply to the score. <br> One of
                'NONE,' 'SOFTMAX,' 'LOGISTIC,' 'SOFTMAX_ZERO,' or 'PROBIT.'
        """

        schema = get_schema("TreeEnsembleClassifier", 1, "ai.onnx.ml")
        op = Op(self, "TreeEnsembleClassifier", schema)
        return op(
            *self._prepare_inputs(schema, X),
            base_values=base_values,
            class_ids=class_ids,
            class_nodeids=class_nodeids,
            class_treeids=class_treeids,
            class_weights=class_weights,
            classlabels_int64s=classlabels_int64s,
            classlabels_strings=classlabels_strings,
            nodes_falsenodeids=nodes_falsenodeids,
            nodes_featureids=nodes_featureids,
            nodes_hitrates=nodes_hitrates,
            nodes_missing_value_tracks_true=nodes_missing_value_tracks_true,
            nodes_modes=nodes_modes,
            nodes_nodeids=nodes_nodeids,
            nodes_treeids=nodes_treeids,
            nodes_truenodeids=nodes_truenodeids,
            nodes_values=nodes_values,
            post_transform=post_transform,
        )

    T_TreeEnsembleRegressor = TypeVar("T_TreeEnsembleRegressor", DOUBLE, FLOAT, INT32, INT64)

    def TreeEnsembleRegressor(
        self,
        X: T_TreeEnsembleRegressor,
        *,
        aggregate_function: str = "SUM",
        base_values: Optional[Sequence[float]] = None,
        n_targets: Optional[int] = None,
        nodes_falsenodeids: Optional[Sequence[int]] = None,
        nodes_featureids: Optional[Sequence[int]] = None,
        nodes_hitrates: Optional[Sequence[float]] = None,
        nodes_missing_value_tracks_true: Optional[Sequence[int]] = None,
        nodes_modes: Optional[Sequence[str]] = None,
        nodes_nodeids: Optional[Sequence[int]] = None,
        nodes_treeids: Optional[Sequence[int]] = None,
        nodes_truenodeids: Optional[Sequence[int]] = None,
        nodes_values: Optional[Sequence[float]] = None,
        post_transform: str = "NONE",
        target_ids: Optional[Sequence[int]] = None,
        target_nodeids: Optional[Sequence[int]] = None,
        target_treeids: Optional[Sequence[int]] = None,
        target_weights: Optional[Sequence[float]] = None,
    ) -> FLOAT:
        r"""[🌐 ai.onnx.ml::TreeEnsembleRegressor(1)](https://onnx.ai/onnx/operators/onnx_aionnxml_TreeEnsembleRegressor.html#treeensembleregressor-1 "Online Documentation")


            Tree Ensemble regressor.  Returns the regressed values for each input in N.

            All args with nodes_ are fields of a tuple of tree nodes, and
            it is assumed they are the same length, and an index i will decode the
            tuple across these inputs.  Each node id can appear only once
            for each tree id.

            All fields prefixed with target_ are tuples of votes at the leaves.

            A leaf may have multiple votes, where each vote is weighted by
            the associated target_weights index.

            All trees must have their node ids start at 0 and increment by 1.

            Mode enum is BRANCH_LEQ, BRANCH_LT, BRANCH_GTE, BRANCH_GT, BRANCH_EQ, BRANCH_NEQ, LEAF


        Args:
            X: Input of shape [N,F]

            aggregate_function: Defines how to aggregate leaf values within a target.
                <br>One of 'AVERAGE,' 'SUM,' 'MIN,' 'MAX.'

            base_values: Base values for classification, added to final class score; the
                size must be the same as the classes or can be left unassigned (assumed
                0)

            n_targets: The total number of targets.

            nodes_falsenodeids: Child node if expression is false

            nodes_featureids: Feature id for each node.

            nodes_hitrates: Popularity of each node, used for performance and may be
                omitted.

            nodes_missing_value_tracks_true: For each node, define what to do in the
                presence of a NaN: use the 'true' (if the attribute value is 1) or
                'false' (if the attribute value is 0) branch based on the value in this
                array.<br>This attribute may be left undefined and the defalt value is
                false (0) for all nodes.

            nodes_modes: The node kind, that is, the comparison to make at the node.
                There is no comparison to make at a leaf node.<br>One of 'BRANCH_LEQ',
                'BRANCH_LT', 'BRANCH_GTE', 'BRANCH_GT', 'BRANCH_EQ', 'BRANCH_NEQ',
                'LEAF'

            nodes_nodeids: Node id for each node. Node ids must restart at zero for each
                tree and increase sequentially.

            nodes_treeids: Tree id for each node.

            nodes_truenodeids: Child node if expression is true

            nodes_values: Thresholds to do the splitting on for each node.

            post_transform: Indicates the transform to apply to the score. <br>One of
                'NONE,' 'SOFTMAX,' 'LOGISTIC,' 'SOFTMAX_ZERO,' or 'PROBIT'

            target_ids: The index of the target that each weight is for

            target_nodeids: The node id of each weight

            target_treeids: The id of the tree that each node is in.

            target_weights: The weight for each target
        """

        schema = get_schema("TreeEnsembleRegressor", 1, "ai.onnx.ml")
        op = Op(self, "TreeEnsembleRegressor", schema)
        return op(
            *self._prepare_inputs(schema, X),
            aggregate_function=aggregate_function,
            base_values=base_values,
            n_targets=n_targets,
            nodes_falsenodeids=nodes_falsenodeids,
            nodes_featureids=nodes_featureids,
            nodes_hitrates=nodes_hitrates,
            nodes_missing_value_tracks_true=nodes_missing_value_tracks_true,
            nodes_modes=nodes_modes,
            nodes_nodeids=nodes_nodeids,
            nodes_treeids=nodes_treeids,
            nodes_truenodeids=nodes_truenodeids,
            nodes_values=nodes_values,
            post_transform=post_transform,
            target_ids=target_ids,
            target_nodeids=target_nodeids,
            target_treeids=target_treeids,
            target_weights=target_weights,
        )

    T_ZipMap: TypeAlias = Union[Sequence[Mapping[int, FLOAT]], Sequence[Mapping[str, FLOAT]]]

    def ZipMap(
        self,
        X: FLOAT,
        *,
        classlabels_int64s: Optional[Sequence[int]] = None,
        classlabels_strings: Optional[Sequence[str]] = None,
    ) -> T_ZipMap:
        r"""[🌐 ai.onnx.ml::ZipMap(1)](https://onnx.ai/onnx/operators/onnx_aionnxml_ZipMap.html#zipmap-1 "Online Documentation")


            Creates a map from the input and the attributes.

            The values are provided by the input tensor, while the keys are specified by the attributes.
            Must provide keys in either classlabels_strings or classlabels_int64s (but not both).

            The columns of the tensor correspond one-by-one to the keys specified by the attributes. There must be as many columns as keys.



        Args:
            X: The input values

            classlabels_int64s: The keys when using int keys.<br>One and only one of the
                'classlabels_*' attributes must be defined.

            classlabels_strings: The keys when using string keys.<br>One and only one of
                the 'classlabels_*' attributes must be defined.
        """

        schema = get_schema("ZipMap", 1, "ai.onnx.ml")
        op = Op(self, "ZipMap", schema)
        return op(
            *self._prepare_inputs(schema, X),
            classlabels_int64s=classlabels_int64s,
            classlabels_strings=classlabels_strings,
        )
