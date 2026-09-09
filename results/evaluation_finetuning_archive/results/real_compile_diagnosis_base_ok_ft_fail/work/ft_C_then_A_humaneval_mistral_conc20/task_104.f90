program unique_digits_demo
  implicit none
  integer, parameter :: dp = kind(1.0d0)
  integer :: x_len
  integer, allocatable :: x(:)
  integer, allocatable :: result(:)
  integer :: i

  ! Hardcoded input as per example
  x_len = 4
  allocate(x(x_len))
  x = [15, 33, 1422, 1]

  ! Call the function
  result = unique_digits(x_len, x)

  ! Output the result
  print *, 'Result:', result

contains

  function unique_digits(x_len, x) result(res)
    implicit none
    integer, intent(in) :: x_len
    integer, intent(in) :: x(x_len)
    integer, allocatable :: res(:)
    integer :: i, n, j
    logical :: contains_even

    ! Initialize result array
    allocate(res(x_len))
    n = 0
    do i = 1, x_len
      if (.not. contains_even_digit(x(i))) then
        n = n + 1
      end if
    end do
    allocate(res(n))
    j = 0
    do i = 1, x_len
      if (.not. contains_even_digit(x(i))) then
        j = j + 1
        res(j) = x(i)
      end if
    end do
  end function unique_digits

  function contains_even_digit(num) result(has_even)
    implicit none
    integer, intent(in) :: num
    logical :: has_even
    integer :: temp, digit

    if (num == 0) then
      has_even = .true.
      return
    end if
    temp = abs(num)
    do while (temp > 0)
      digit = mod(temp, 10)
      if (mod(digit, 2) == 0) then
        has_even = .true.
        return
      end if
      temp = temp / 10
    end do
    has_even = .false.
  end function contains_even_digit

end program unique_digits_demo