program digits
  implicit none
  integer :: n, result

  ! Read input
  read *, n

  ! Calculate result
  result = digits(n)

  ! Output result
  print *, result

contains

  function digits(n) result(res)
    implicit none
    integer, intent(in) :: n
    integer :: res
    integer :: i, digit, product
    character(len=10) :: num_str

    ! Convert number to string
    write(num_str, '(I0)') n

    ! Calculate product of odd digits
    product = 1
    do i = 1, len(num_str)
      digit = iachar(num_str(i:i)) - iachar('0')
      if (mod(digit, 2) == 1) then
        product = product * digit
      end if
    end do

    res = product
  end function digits

end program digits