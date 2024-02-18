"""Hidden module for the sisetup class.

"""
from . number import _parse_number
from . unit import _parse_unit, _unit_kw

from typing import Any, Dict, Literal



class sisetup():
    """Set up mplunitx with the desired options.

    Creating an instance of the `sisetup` class provides access to the
    methods `num`, `unit`, `qty`, and `label`.
    With the parameters a variety of options can be set to customize the
    output of the methods.

    The set options can be temporarily overwritten in the method calls. 

    Parameters
    ----------
    declare_unit : dict, optional
        Additional units can be declared using this parameter. The keys
        are the unit names and the values are the LaTeX representation;
        e.g. ``{"arbitraryunit": r"arb.\,u."}``.

    Attributes
    ----------
    declare_unit : dict
        Dictionary that stores units declared by the user.
    unit_kw : mplunitx.unit._unit_kw
        Instance of `mplunitx.unit._unit_kw` containing the unit
        formatting options.

    Other Parameters
    ----------------
    inter_unit_product : str, default=r"\\\,"
        Character used to separate units.
    per_mode : str, default="power"
        Mode for typesetting units with negative power.
        Must be one of ``{"power", "fraction", "symbol",
        "single-symbol", "power-positive-first"}``.
        ``"power"``: Units are typeset with positive and negative
        powers. ``"fraction"``: Units are typeset as a fraction using
        ``\\frac``. ``"symbol"``: Units are typeset with a character
        between positive and negative powers (Default: ``"/"``, see
        `per_symbol`). ``"single-symbol"``: Units are typeset like
        ``"symbol"`` if there is only one unit with negative power.
        Otherwise powers are used. ``"power-positive-first"``: Units are
        typeset like ``"power"`` but positive powers are typeset left of
        negative powers.
    per_symbol : str, default="/"
        Character between positive and negative powers when in
        ``"symbol"`` or ``"single-symbol"`` mode.
    bracket_unit_denominator : bool, default=True
        If ``True`` and in ``"symbol"`` mode encloses the units to the
        right of the symbol in brackets.
    per_symbol_script_correction : str, default=r"\\\!"
        If the character before ``per_symbol`` is a power, the space
        between the power and the symbol is corrected using the given
        string.
    sticky_per : bool, default=False
        Not implemented yet.
    parse_units : bool, default=True
        If ``False`` the input string is returned as is.
    unit_font_command : str, default=r"\\\mathrm"
        LaTeX command used to typeset units.
    quantity_product : str, default=r"\\\,"
        Character used to separate number and unit.
    label_unit_mode : str, default="/"
        Must be one of ``{"/", "[]"}``. If ``"/"`` the variable and unit
        are separated by a forward slash when using the `label` method.
        If ``"[]"`` the unit is enclosed in square brackets.

    Examples
    --------
    Import the module and create an instance of the `sisetup` class:

    >>> from mplunitx import sisetup
    >>> si = sisetup()

    Use the `label` method to typeset a label:

    >>> si.label("Energy", "mega.eV")
    'Energy$\\;/\\;\\mathrm{MeV}$'

    And use it to label a matplotlib plot:

    >>> import matplotlib.pyplot as plt
    >>> plt.plot([100, 200, 300], [1, 2, 3])
    >>> plt.xlabel(si.label("Measurement duraction", "day"))
    >>> plt.ylabel(si.label("Integrated luminosity", "per.femto.barn"))
    
    """
    per_mode_options = ["power", "fraction", "symbol", "single-symbol",
                        "power-positive-first"]
    label_unit_mode_options = ["/", "[]"]

    def __init__(
        self,
        declare_unit: Dict[str, str] = None,
        inter_unit_product: str = r"\,",
        per_mode: Literal["power", "fraction", "symbol", "single-symbol",
                          "power-positive-first"] = "power",
        per_symbol: str = "/",
        bracket_unit_denominator: bool = True,
        per_symbol_script_correction: str = r"\!",
        sticky_per: bool = False,
        parse_units: bool = True,
        unit_font_command: str = r"\mathrm",
        quantity_product: str = r"\,",
        label_unit_mode: Literal["/", "[]"] = "/"
    ):
        # declare units
        if declare_unit is not None:
            if not isinstance(declare_unit, dict):
                raise TypeError("declare_unit must be a dict.")
            for k, v in declare_unit.items():
                if not isinstance(k, str) or not isinstance(v, str):
                    raise TypeError("declare_unit must be a dict of str.")
        self.declare_unit = declare_unit

        # options unit
        self.unit_kw = _unit_kw(
            inter_unit_product=inter_unit_product,
            per_mode=per_mode,
            per_symbol=per_symbol,
            bracket_unit_denominator=bracket_unit_denominator,
            per_symbol_script_correction=per_symbol_script_correction,
            sticky_per=sticky_per,
            parse_units=parse_units,
            unit_font_command=unit_font_command
        )

        # options qty
        self.quantity_product = quantity_product

        # options label
        self.label_unit_mode = label_unit_mode


    @property
    def quantity_product(self) -> str:
        return self._quantity_product

    @quantity_product.setter
    def quantity_product(self, val: str):
        if isinstance(val, str):
            self._quantity_product = val
        else:
            raise ValueError("quantity_product must be a str.")


    @property
    def label_unit_mode(self) -> Literal["/", "[]"]:
        return self._label_unit_mode

    @label_unit_mode.setter
    def label_unit_mode(self, val: Literal["/", "[]"]):
        if val in self.label_unit_mode_options:
            self._label_unit_mode = val
        else:
            raise ValueError("label_unit_mode must be on of "
                             "label_unit_mode_options.")


    def num(self, number: str) -> str:
        """Dummy implementation.

        Returns given string with ``"$"`` around.

        """
        tex_str = _parse_number(number)
        return "$" + tex_str + "$"


    def unit(self, unit: str, **unit_kw) -> str:
        """Returns the LaTeX code for the given unit.

        Parameters
        ----------
        unit : str
            The unit to be typeset as a string. Multiple units can be
            combined using a semicolon ``";"`` inbetween. The units can
            be combined with a prefix, e.g. ``"kilo.meter"`` and a
            power, which can be specified by either a number or key
            word again seperated with a dot ``"."``. The following
            examples are equivalent: ``"kilo.meter.-2"``,
            ``"per.kilo.meter.2"``, ``"per.kilo.meter.squared"``,
            ``"per.square.kilo.meter"``.
        **unit_kw
            Keyword arguments to overwrite the options in
            `sisetup.unit_kw`. The options are only overwritten for this
            call.

        Returns
        -------
        str
            The LaTeX code for the given unit.

        Examples
        --------

        >>> from mplunitx import sisetup
        >>> si = sisetup()
        >>> si.unit("per.square.kilo.meter")
        '$\\mathrm{km}^{-2}$'

        """
        if not isinstance(unit, str):
            raise TypeError("unit must be a string.")
        
        kw = _unit_kw(**self.unit_kw._unit_kw)
        if unit_kw is not None:
            kw.update(unit_kw)

        if not kw.parse_units:
            return unit

        unit = unit.split(";")

        if kw.per_mode != "power":
            # If per_mode is fraction add \frac{ 
            if kw.per_mode == "fraction":
                tex_str = r"\frac{"
            else:
                tex_str = ""

            # Add all units to str with positive power
            count_pos = 0
            for i, u in enumerate(unit):
                utex, power = _parse_unit(
                    u, user_declared_units=self.declare_unit)
                if power > 0:
                    tex_str += utex
                    if power != 1:
                        tex_str += "^{" + str(power) + "}"
                    tex_str += kw.inter_unit_product
                    count_pos += 1

            # Add str between pos and neg power
            if kw.per_mode == "fraction":
                tex_str = tex_str[:-len(kw.inter_unit_product)]
                tex_str += "}{"
            elif kw.per_mode in ["symbol", "single-symbol"]:
                tex_str = tex_str[:-len(kw.inter_unit_product)]
                if tex_str[-2].isdigit():
                    tex_str += kw.per_symbol_script_correction
                tex_str += kw.per_symbol
                if kw.bracket_unit_denominator:
                    tex_str += "("

            # Add all units to str with negative power
            count_neg = 0
            for i, u in enumerate(unit):
                utex, power = _parse_unit(
                    u, user_declared_units=self.declare_unit)
                if power < 0:
                    tex_str += utex
                    if (kw.per_mode in 
                        ["symbol", "single-symbol", "fraction"]):
                        if power != -1:   
                            tex_str += "^{" + str(-power) + "}"
                    else:      
                        tex_str += "^{" + str(power) + "}"
                    tex_str += kw.inter_unit_product
                    count_neg += 1

            tex_str = tex_str[:-len(kw.inter_unit_product)]
            if kw.per_mode == "fraction":
                tex_str += "}"
            if (kw.per_mode in ["symbol", "single-symbol"] 
                and kw.bracket_unit_denominator):
                if count_neg > 1:
                    tex_str += ")"
                else:
                    tex_str = tex_str.replace("(", "")

        # If per_mode is power or single-symbol and count_neg > 1
        if kw.per_mode == "power" or (kw.per_mode == "single-symbol"
                                        and count_neg > 1):
            tex_str = ""
            for i, u in enumerate(unit):
                utex, power = _parse_unit(
                    u, user_declared_units=self.declare_unit)
                tex_str += utex
                if power != 1:
                    tex_str += "^{" + str(power) + "}"
                if i < len(unit) - 1:
                    tex_str += kw.inter_unit_product
        
        return "$" + tex_str + "$"


    def qty(self, number: str, unit: str, unit_kw: Dict[str, Any] = None,
            **qty_kw) -> str:
        """Returns the LaTeX code for the given quantity.

        Combines a number and a unit to a string containing the LaTeX
        code.

        Parameters
        ----------
        number : str
            The number to be typeset passed to the `num` method.
        unit : str
            The unit to be typeset passed to the `unit` method.
        unit_kw : dict, optional
            Dictionary containing keyword arguments to temporarily
            overwrite the options in `sisetup.unit_kw`.
        **qty_kw
            Not implemented yet.

        Returns
        -------
        str
            The LaTeX code for the given quantity.

        """
        number = self.num(number).replace("$", "")

        if unit_kw is None:
            unit = self.unit(unit).replace("$", "")
        else:
            unit = self.unit(unit, **unit_kw).replace("$", "")

        first_unit = unit.find("{") + 1
        if unit[first_unit] == "'":
            return "$" + number + unit + "$"
        elif unit[first_unit] == "◦" and unit[first_unit+1] != "C":
            return "$" + number + unit + "$"

        return "$" + number + self.quantity_product + unit + "$"


    def label(self, var: str, unit: str, var_font_command="") -> str:
        """Returns a string containing the LaTeX code of a figure label
        constructed from a variable name und unit.

        Parameters
        ----------
        var : str
            The variable name.
        unit : str
            The unit to be typeset passed to the `unit` method.

        Returns
        -------
        str
            The LaTeX code for the given label.

        """
        if not isinstance(var, str):
            raise TypeError("var must be a string.")

        unit = self.unit(unit).replace("$", "")

        if self.label_unit_mode == "/":
            return "$" + var_font_command + "{" + var + r"}\;/\;" + unit + "$"
        elif self.label_unit_mode == "[]":
            return "$" + var_font_command + "{" + var + r"}\;[" + unit + "]$"
