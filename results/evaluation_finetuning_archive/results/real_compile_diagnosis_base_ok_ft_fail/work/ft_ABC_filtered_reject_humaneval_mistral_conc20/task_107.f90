program even_odd_palindrome
  implicit none
  integer :: n
  integer :: even_count, odd_count
  integer :: i
  integer :: temp
  character(len=10) :: str, rev_str
  logical :: is_palindrome

  ! Read input
  read(*,*) n

  even_count = 0
  odd_count = 0

  do i = 1, n
    temp = i
    str = ''
    do while (temp > 0)
      str = trim(str) // char(mod(temp, 10) + 48)
      temp = temp / 10
    end do
    rev_str = ''
    do i = len(str), 1, -1
      rev_str = trim(rev_str) // str(i:i)
    end do
    if (str == rev_str) then
      if (mod(i, 2) == 0) then
        even_count = even_count + 1
      else
        odd_count = odd_count + 1
      end if
    end if
  end do

  print *, even_count, odd_count
end program even_odd_palindrome