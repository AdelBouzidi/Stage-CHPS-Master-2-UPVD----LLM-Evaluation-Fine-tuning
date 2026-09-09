program vowels_count_demo
  implicit none
  integer :: count
  character(len=100) :: input_string

  ! Read input from stdin
  read(*, '(a)') input_string

  ! Count vowels using the function
  count = vowels_count(input_string)

  ! Write output to stdout
  write(*, '(i0)') count

contains

  function vowels_count(s) result(count)
    implicit none
    character(len=*), intent(in) :: s
    integer :: count
    integer :: i
    character(len=1) :: c

    count = 0
    do i = 1, len_trim(s)
      c = s(i:i)
      if (index('aeiouAEIOU', c) > 0) then
        count = count + 1
      else if (c == 'y' .or. c == 'Y') then
        if (i == len_trim(s)) then
          count = count + 1
        end if
      end if
    end do
  end function vowels_count

end program vowels_count_demo