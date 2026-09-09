program even_odd_palindrome
  implicit none
  integer :: n
  integer :: even_count, odd_count
  integer :: i
  integer :: temp, digit_count, digits(10)
  logical :: is_palindrome

  ! Read input
  read(*,*) n

  ! Initialize counters
  even_count = 0
  odd_count = 0

  ! Check each number from 1 to n
  do i = 1, n
    if (is_palindrome(i)) then
      if (mod(i, 2) == 0) then
        even_count = even_count + 1
      else
        odd_count = odd_count + 1
      end if
    end if
  end do

  ! Output results
  print *, even_count, odd_count

contains

  function is_palindrome(num) result(is_pal)
    integer, intent(in) :: num
    logical :: is_pal
    integer :: temp, digit_count, digits(10)

    if (num < 0) then
      is_pal = .false.
      return
    end if

    if (num == 0) then
      is_pal = .true.
      return
    end if

    ! Extract digits
    temp = num
    digit_count = 0
    do while (temp > 0)
      digit_count = digit_count + 1
      digits(digit_count) = mod(temp, 10)
      temp = temp / 10
    end do

    ! Check if palindrome
    is_pal = .true.
    do i = 1, digit_count / 2
      if (digits(i) /= digits(digit_count - i + 1)) then
        is_pal = .false.
        exit
      end if
    end do

  end function is_palindrome

end program even_odd_palindrome