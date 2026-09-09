program factorize_demo
  implicit none
  integer :: n
  integer, allocatable :: factors(:)

  ! Hardcoded input value
  n = 8

  ! Call the factorize function
  factors = factorize(n)

  ! Print the result
  print *, 'Factors of', n, ':', factors

contains

  function factorize(n) result(factors)
    implicit none
    integer, intent(in) :: n
    integer, allocatable :: factors(:)
    integer :: i, count
    integer :: temp

    if (n <= 1) then
      allocate(factors(0))
      return
    end if

    allocate(factors(0))
    temp = n
    i = 2
    do while (i * i <= temp)
      count = 0
      do while (mod(temp, i) == 0)
        count = count + 1
        temp = temp / i
      end do
      if (count > 0) then
        allocate(factors(size(factors) + count))
        factors(size(factors) + 1 : size(factors) + count) = i
      end if
      i = i + 1
    end do
    if (temp > 1) then
      allocate(factors(size(factors) + 1))
      factors(size(factors) + 1) = temp
    end if
  end function factorize

end program factorize_demo