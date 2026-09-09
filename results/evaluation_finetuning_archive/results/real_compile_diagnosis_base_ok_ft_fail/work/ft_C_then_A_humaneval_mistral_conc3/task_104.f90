program unique_digits_demo
  implicit none
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
    integer :: i, j, n, temp
    logical :: contains_even

    ! Initialize result array
    allocate(res(x_len))
    n = 0
    do i = 1, x_len
      if (.not. contains_even_digit(x(i))) then
        n = n + 1
        res(n) = x(i)
      end if
    end do

    ! Sort the result array
    do i = 1, n-1
      do j = i+1, n
        if (res(i) > res(j)) then
          temp = res(i)
          res(i) = res(j)
          res(j) = temp
        end if
      end do
    end do

    ! Resize result array to actual size
    if (allocated(res)) deallocate(res)
    allocate(res(n))
    res = res(1:n)

  end function unique_digits

  function contains_even_digit(num) result(has_even)
    implicit none
    integer, intent(in) :: num
    logical :: has_even
    integer :: digit

    has_even = .false.
    do while (num > 0)
      digit = mod(num, 10)
      if (mod(digit, 2) == 0) then
        has_even = .true.
        exit
      end if
      num = num / 10
    end do
  end function contains_even_digit

end program unique_digits_demo